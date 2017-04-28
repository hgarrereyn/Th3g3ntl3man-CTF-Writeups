# ETA?
#### Writeup by hgarrereyn
* **Reverse Engineering**
* *60 points*
* Description: If this script were to finish, what would it output? MacOS Linux

# Solution

After running the script and watching the prompt hang for 30 seconds, it is pretty clear that the script would either hang forever or take an inordinate amount of time to finish. Rather than solve the halting problem, I opted to do some dynamic analysis.

I viewed the disassembly in Hopper and tried to find the part of the code that was causing the program to hang.

Early on in `main`, I found the following function call:

```asm
0000000000400dac         lea        rax, qword [rbp+var_40]
0000000000400db0         mov        esi, 0x7ffffffc
0000000000400db5         mov        rdi, rax                                    ; argument #1 for method _Z10get_primesm
0000000000400db8         call       _Z10get_primesm
```

Hmm, maybe this could be the problem. Let's find out. I'll set a breakpoint after the function call and see if we hit it.

```
$ gdb -q eta
Reading symbols from eta...(no debugging symbols found)...done.
(gdb) b *0x400dbd
Breakpoint 1 at 0x400dbd
(gdb) r
Starting program: /home/ubuntu/pactf/eta

Breakpoint 1, 0x0000000000400dbd in main ()
```

We hit the breakpoint after about a minute so this isn't the problem.

*Side note: I actually found this out on accident by running the program assuming it would hang on the `get_primes` function. I switched windows and started googling something and when I switched back in a few minutes, it had reached the breakpoint.*

Next we see some sort of loop followed by an `ostream` call to print something to the console.

```asm
0000000000400ddc         mov        qword [rbp+var_70], 0x0
0000000000400de4         mov        dword [rbp+var_14], 0x0
0000000000400deb         mov        dword [rbp+var_18], 0x0

                     loc_400df2:
0000000000400df2         cmp        dword [rbp+var_18], 0xf423f                 ; CODE XREF=main+196
0000000000400df9         jg         loc_400e5d

0000000000400dfb         lea        rax, qword [rbp+var_60]
0000000000400dff         mov        rdi, rax
0000000000400e02         call       _ZNSt6vectorImSaImEE5beginEv                ; std::vector<unsigned long, std::allocator<unsigned long> >::begin()
0000000000400e07         mov        qword [rbp+var_70], rax

                     loc_400e0b:
0000000000400e0b         lea        rax, qword [rbp+var_60]                     ; CODE XREF=main+190
0000000000400e0f         mov        rdi, rax
0000000000400e12         call       _ZNSt6vectorImSaImEE3endEv                  ; std::vector<unsigned long, std::allocator<unsigned long> >::end()
0000000000400e17         mov        qword [rbp+var_20], rax
0000000000400e1b         lea        rdx, qword [rbp+var_20]
0000000000400e1f         lea        rax, qword [rbp+var_70]
0000000000400e23         mov        rsi, rdx                                    ; argument #2 for method _ZN9__gnu_cxxltIPmSt6vectorImSaImEEEEbRKNS_17__normal_iteratorIT_T0_EESA_
0000000000400e26         mov        rdi, rax                                    ; argument #1 for method _ZN9__gnu_cxxltIPmSt6vectorImSaImEEEEbRKNS_17__normal_iteratorIT_T0_EESA_
0000000000400e29         call       _ZN9__gnu_cxxltIPmSt6vectorImSaImEEEEbRKNS_17__normal_iteratorIT_T0_EESA_ ; bool __gnu_cxx::operator< <unsigned long*, std::vector<unsigned long, std::allocator<unsigned long> > >(__gnu_cxx::__normal_iterator<unsigned long*, std::vector<unsigned long, std::allocator<unsigned long> > > const&, __gnu_cxx::__normal_iterator<unsigned long*, std::vector<unsigned long, std::allocator<unsigned long> > > const&)
0000000000400e2e         test       al, al
0000000000400e30         je         loc_400e57

0000000000400e32         lea        rax, qword [rbp+var_70]
0000000000400e36         mov        rdi, rax
0000000000400e39         call       _ZNK9__gnu_cxx17__normal_iteratorIPmSt6vectorImSaImEEEdeEv ; __gnu_cxx::__normal_iterator<unsigned long*, std::vector<unsigned long, std::allocator<unsigned long> > >::operator*() const
0000000000400e3e         mov        rax, qword [rax]
0000000000400e41         mov        dword [rbp+var_14], eax
0000000000400e44         lea        rax, qword [rbp+var_70]
0000000000400e48         mov        esi, 0x0
0000000000400e4d         mov        rdi, rax                                    ; argument #1 for method _ZN9__gnu_cxx17__normal_iteratorIPmSt6vectorImSaImEEEppEi
0000000000400e50         call       _ZN9__gnu_cxx17__normal_iteratorIPmSt6vectorImSaImEEEppEi ; __gnu_cxx::__normal_iterator<unsigned long*, std::vector<unsigned long, std::allocator<unsigned long> > >::operator++(int)
0000000000400e55         jmp        loc_400e0b

                     loc_400e57:
0000000000400e57         add        dword [rbp+var_18], 0x1                     ; CODE XREF=main+153
0000000000400e5b         jmp        loc_400df2
```

The loop counter (`var_18`) is initialized to zero and incremented each loop. The loop will terminate once it reaches `0xf423f` or `999999`. We also see a bunch of vector initializations going on in the loop. So this must be where we are hanging.

The print is performed by the following (outside of the loop):

```asm
					loc_400e5d:
0000000000400e5d         mov        eax, dword [rbp+var_14]                     ; CODE XREF=main+98
0000000000400e60         mov        esi, eax
0000000000400e62         mov        edi, 0x602ea0
0000000000400e67         call       j__ZNSolsEi
0000000000400e6c         mov        esi, 0x400b00
0000000000400e71         mov        rdi, rax
0000000000400e74         call       j__ZNSolsEPFRSoS_E
```

So we see that `var_14` gets printed (`$rbp-20`). Also, we notice that the same variable is written to inside the loop. Let's examine a few iterations to see if we can find out what it is set to.

```
$ gdb -q eta
Reading symbols from eta...(no debugging symbols found)...done.
(gdb) b *0x400df2
Breakpoint 1 at 0x400df2
(gdb) define hook-stop
Type commands for definition of "hook-stop".
End with a line saying just "end".
>x/x $rbp-20
>end
(gdb) r
Starting program: /home/ubuntu/pactf/eta
0x7fffffffe51c:	0x00000000

Breakpoint 1, 0x0000000000400df2 in main ()
(gdb) c
Continuing.
0x7fffffffe51c:	0x7fffffed

Breakpoint 1, 0x0000000000400df2 in main ()
(gdb) c
Continuing.
0x7fffffffe51c:	0x7fffffed

Breakpoint 1, 0x0000000000400df2 in main ()
(gdb) c
Continuing.
0x7fffffffe51c:	0x7fffffed

Breakpoint 1, 0x0000000000400df2 in main ()
```

Hmm, it doesn't seem to change. Every loop, it is set to `0x7fffffed` or `2147483629`.

So the flag must be `2147483629`.
