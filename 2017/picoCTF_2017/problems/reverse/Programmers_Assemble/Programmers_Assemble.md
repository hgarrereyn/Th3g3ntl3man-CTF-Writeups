# Programmers Assemble
#### Writeup by hgarrereyn
* **Reverse Engineering**
* *75 points*
* Description: You found a text [file](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/raw/0e4c994d51130f747bf8d9932274cb85e3f0f1c5/2017/picoCTF_2017/problems/reverse/Programmers_Assemble/assembly.s) with some really low level code. Some value at the beginning has been X'ed out. Can you figure out what should be there, to make main return the value 0x1? Submit the answer as a hexidecimal number, with no extraneous 0s. For example, the decimal number 2015 would be submitted as 0x7df, not 0x000007df

# Links

Here is the file we were given:

[**assembly.s**](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/raw/0e4c994d51130f747bf8d9932274cb85e3f0f1c5/2017/picoCTF_2017/problems/reverse/Programmers_Assemble/assembly.s)

```asm
.global main

main:
    mov $XXXXXXX, %eax
    mov $0, %ebx
    mov $0x8, %ecx
loop:
    test %eax, %eax
    jz fin
    add %ecx, %ebx
    dec %eax
    jmp loop
fin:
    cmp $0xb790, %ebx
    je good
    mov $0, %eax
    jmp end
good:
    mov $1, %eax
end:
    ret
```

# Solution

We are looking for a return value of `0x1`. The only place we get this is in the `good` subroutine.

Looking backwards through the assembly, we see that the only code that branches here is in the `fin` subroutine. Therefore, `%ebx` must equal `0xb790` when we call `fin`. But where do we branch to `fin`?

Well, it looks like there is a `loop` subroutine that will call fin when `%eax` is zero. Otherwise, it will do the following operations:
* `%ebx += %ecx`
* `%eax -= 1`

So essentially, we are looking at a subroutine that will add `%ecx` to `%ebx` `%eax` times. We can represent this with a simple multiplication equation. By the time we call `fin`, `%ebx += (%eax * %ecx)`. We have to find `%eax` so what are those other values?

Well, in `main`, we initialize `%ebx` to zero and `%ecx` to `0x8`. Therefore our equation looks like this: `%ebx = 0x8 * %eax`.

In order to return 1, `%ebx` must be `0xb790` so we obtain: `0xb790 = 0x8 * %eax` which simplifies to: `%eax = 0x16f2`.

We submit this value as the flag.

Flag: `0x16f2`
