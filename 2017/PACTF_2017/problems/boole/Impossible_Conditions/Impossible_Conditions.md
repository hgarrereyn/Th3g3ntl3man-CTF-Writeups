# Impossible Conditions
#### Writeup by hgarrereyn
* **Reverse Engineering**
* *30 points*
* Let’s make the impossible possible! Let’s make 1=5. [impossible.out](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/raw/ec055096672b3ca26df1a600ae572486e5db4bc9/2017/PACTF_2017/problems/boole/Impossible_Conditions/impossible)

# Solution

Running this binary produces no output and exits immediately. Let's take a look at the disassembly.

First we notice a bunch of suspicious `mov` operations that appear to be swapping some char codes around.

Then we see some `get_time` methods right before a `je` (line `0x401420`) that skips a large chunk of code:

```asm
					main:
0000000000400e06         push       rbp                                         ; DATA XREF=_start+29
0000000000400e07         mov        rbp, rsp
0000000000400e0a         push       r15
0000000000400e0c         push       r14
0000000000400e0e         push       r13
0000000000400e10         push       r12
0000000000400e12         push       rbx
0000000000400e13         sub        rsp, 0x1e8
0000000000400e1a         mov        rax, qword [fs:0x28]
0000000000400e23         mov        qword [rbp+var_38], rax
0000000000400e27         xor        eax, eax
0000000000400e29         mov        byte [m], 0x6d
0000000000400e30         mov        byte [n], 0x6e
0000000000400e37         mov        byte [z], 0x7a
					<many lines omitted>
0000000000401362         mov        byte [z], 0x21
0000000000401369         mov        byte [n], 0x6e
0000000000401370         mov        byte [x], 0x78
0000000000401377         lea        rax, qword [rbp+var_1F0]
000000000040137e         mov        esi, 0x0                                    ; argument "tzp" for method j_gettimeofday
0000000000401383         mov        rdi, rax                                    ; argument "tp" for method j_gettimeofday
0000000000401386         call       j_gettimeofday
000000000040138b         mov        rax, qword [rbp+var_1F0]
0000000000401392         mov        qword [rbp+var_1F8], rax
0000000000401399         lea        rax, qword [rbp+var_1F8]
00000000004013a0         mov        rdi, rax                                    ; argument "clock" for method j_localtime
00000000004013a3         call       j_localtime
00000000004013a8         mov        rdx, rax
00000000004013ab         lea        rax, qword [rbp+var_60]
00000000004013af         mov        rcx, rdx                                    ; argument "timeptr" for method j_strftime
00000000004013b2         mov        edx, 0x401a54                               ; "%m-%d-%Y\\t%T.", argument "format" for method j_strftime
00000000004013b7         mov        esi, 0x1e                                   ; argument "maxsize" for method j_strftime
00000000004013bc         mov        rdi, rax                                    ; argument "s" for method j_strftime
00000000004013bf         call       j_strftime
00000000004013c4         lea        rax, qword [rbp+var_1FE]
00000000004013cb         mov        rdi, rax
00000000004013ce         call       j__ZNSaIcEC1Ev
00000000004013d3         lea        rdx, qword [rbp+var_1FE]
00000000004013da         lea        rcx, qword [rbp+var_60]
00000000004013de         lea        rax, qword [rbp+var_80]
00000000004013e2         mov        rsi, rcx
00000000004013e5         mov        rdi, rax
00000000004013e8         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1EPKcRKS3_
00000000004013ed         lea        rax, qword [rbp+var_80]
00000000004013f1         mov        esi, 0x401a61
00000000004013f6         mov        rdi, rax
00000000004013f9         call       j__ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE7compareEPKc
00000000004013fe         test       eax, eax
0000000000401400         sete       bl
0000000000401403         lea        rax, qword [rbp+var_80]
0000000000401407         mov        rdi, rax
000000000040140a         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEED1Ev
000000000040140f         lea        rax, qword [rbp+var_1FE]
0000000000401416         mov        rdi, rax
0000000000401419         call       j__ZNSaIcED1Ev
000000000040141e         test       bl, bl
0000000000401420         je         loc_4017be
0000000000401426         lea        rax, qword [rbp+var_1FE]
000000000040142d         mov        rdi, rax
0000000000401430         call       j__ZNSaIcEC1Ev
...
```

Using gdb we can break at the jump and see if we take it:

```
$ gdb -q impossible
Reading symbols from impossible...(no debugging symbols found)...done.
(gdb) b *0x401420
Breakpoint 1 at 0x401420
(gdb) r
Starting program: /home/ubuntu/pactf/impossible

Breakpoint 1, 0x0000000000401420 in main ()
(gdb) ni
0x00000000004017be in main ()
```

Notice that the instruction pointer did indeed jump to `0x4017be`.

Now, let's use gdb to skip over that `je` and continue execution right after it.

*Note: be sure to set `$rip` not `$eip` since this is a 64 bit binary*

```
$ gdb -q impossible
Reading symbols from impossible...(no debugging symbols found)...done.
(gdb) b *0x401420
Breakpoint 1 at 0x401420
(gdb) r
Starting program: /home/ubuntu/pactf/impossible

Breakpoint 1, 0x0000000000401420 in main ()
(gdb) set $rip=0x401426
(gdb) c
Continuing.
abcx!ilgdn
[Inferior 1 (process 1329) exited normally]
```

Oh look! It printed out something before exiting this time.

That's our flag!

Flag: `abcx!ilgdn`
