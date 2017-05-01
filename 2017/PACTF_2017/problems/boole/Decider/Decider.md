# Decider
#### Writeup by hgarrereyn
* **Reverse Engineering**
* *100 points*
* Decider. [Tie-Breaker](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/raw/ec055096672b3ca26df1a600ae572486e5db4bc9/2017/PACTF_2017/problems/boole/Decider/decider.out) - all u get is that and [this](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/raw/ec055096672b3ca26df1a600ae572486e5db4bc9/2017/PACTF_2017/problems/boole/Decider/daString.txt)

*Note: To reach this problem, you had to take a gamble on a negative 20 point problem.*

# Encrypted flag

[**daString.txt**](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/raw/ec055096672b3ca26df1a600ae572486e5db4bc9/2017/PACTF_2017/problems/boole/Decider/daString.txt)
```
SPQMSQTMSQQMPXYMSPVMSSVMSQWMSQQMPWYMPVPMPWYMPRXMPRQMPWQMSQWMSSSMSQXMSPPMSRSMPYUMPYSMSPRMSSTMSRXMPPYM
```

# Solution

Running the binary multiple times, we see (unfortunately) that the printed string appears to be non-deterministic.

```
$ ./decider
Encrypted To: XQ[E[[[E[XXEXZ[EXYQEXPZE[X_E[Y_EX]YEZZE
$ ./decider
Encrypted To: pysmsssmsppmprsmpqympxrmspwmsqwmpuqmrrm
$ ./decider
Encrypted To: PYSMSSSMSPPMPRSMPQYMPXRMSPWMSQWMPUQMRRM
$ ./decider
Encrypted To: PYSMSSSMSPPMPRSMPQYMPXRMSPWMSQWMPUQMRRM
```

However, after a bit more testing, it seems that certain strings appear repeatedly. So perhaps it is time dependent with a modulus.

At this point, I was uncertain whether the binary itself took any input. It seemed to me like I could get matching outputs even when running with different command line arguments.

Let's take a look at the disassembly.

My first impression was that the `main` subroutine was very long and it appeared that all of the encryption was done in here. It took me awhile to figure out what generally was going on so I'll break it down into a few high-level sections here:

1. Init buffers
2. Encode stored string
3. First pass XOR
4. Second pass XOR

### 1. Init buffers

Here, main sets up a stack frame and initializes some variables and buffers:

```asm
					main:
0000000000401776         push       rbp                                         ; DATA XREF=_start+29
0000000000401777         mov        rbp, rsp
000000000040177a         push       rbx
000000000040177b         sub        rsp, 0xf8
0000000000401782         mov        rax, qword [fs:0x28]
000000000040178b         mov        qword [rbp+var_18], rax
000000000040178f         xor        eax, eax
0000000000401791         lea        rax, qword [rbp+var_F5]
0000000000401798         mov        rdi, rax
000000000040179b         call       j__ZNSaIcEC1Ev
00000000004017a0         lea        rdx, qword [rbp+var_F5]
00000000004017a7         lea        rax, qword [rbp+var_E0]
00000000004017ae         mov        esi, 0x40225c
00000000004017b3         mov        rdi, rax
00000000004017b6         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1EPKcRKS3_
00000000004017bb         lea        rax, qword [rbp+var_F5]
00000000004017c2         mov        rdi, rax
00000000004017c5         call       j__ZNSaIcED1Ev
00000000004017ca         lea        rax, qword [rbp+var_F5]
00000000004017d1         mov        rdi, rax
00000000004017d4         call       j__ZNSaIcEC1Ev
00000000004017d9         lea        rdx, qword [rbp+var_F5]
00000000004017e0         lea        rax, qword [rbp+var_C0]
00000000004017e7         mov        esi, 0x402267
00000000004017ec         mov        rdi, rax
00000000004017ef         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1EPKcRKS3_
00000000004017f4         lea        rax, qword [rbp+var_F5]
00000000004017fb         mov        rdi, rax
00000000004017fe         call       j__ZNSaIcED1Ev
0000000000401803         mov        dword [rbp+var_F4], 0x0
```

The variable `var_C0` (at `$rbp-0xC0`) will be used throughout the program as a pointer to the flag buffer. This buffer will be encoded in a few steps throughout the program.

### 2. Encode stored string

At this point, I realized that the program didn't actually take any input. The string it encodes is hardcoded in the data segment as: `Good Luck!`. *Every output you see is "Good Luck!" being encoded in different ways.*

```asm
loc_40180d:
000000000040180d         mov        eax, dword [rbp+var_F4]                     ; CODE XREF=main+525
0000000000401813         movsxd     rbx, eax
0000000000401816         lea        rax, qword [rbp+var_E0]
000000000040181d         mov        rdi, rax
0000000000401820         call       j__ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6lengthEv
0000000000401825         cmp        rbx, rax
0000000000401828         setb       al
000000000040182b         test       al, al
000000000040182d         je         loc_401988

0000000000401833         mov        eax, dword [rbp+var_F4]
0000000000401839         movsxd     rbx, eax
000000000040183c         lea        rax, qword [rbp+var_E0]
0000000000401843         mov        rdi, rax
0000000000401846         call       j__ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6lengthEv
000000000040184b         sub        rax, 0x1
000000000040184f         cmp        rbx, rax
0000000000401852         sete       al
0000000000401855         test       al, al
0000000000401857         je         loc_4018e0

000000000040185d         mov        eax, dword [rbp+var_F4]
0000000000401863         movsxd     rdx, eax
0000000000401866         lea        rax, qword [rbp+var_E0]
000000000040186d         mov        rsi, rdx
0000000000401870         mov        rdi, rax
0000000000401873         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm
0000000000401878         movzx      eax, byte [rax]
000000000040187b         movsx      edx, al
000000000040187e         lea        rax, qword [rbp+var_A0]
0000000000401885         mov        esi, edx
0000000000401887         mov        rdi, rax                                    ; argument #1 for method _ZNSt7__cxx119to_stringEi
000000000040188a         call       _ZNSt7__cxx119to_stringEi                   ; std::__cxx11::to_string(int)
000000000040188f         lea        rax, qword [rbp+var_80]
0000000000401893         lea        rcx, qword [rbp+var_A0]
000000000040189a         mov        edx, 0x402268
000000000040189f         mov        rsi, rcx                                    ; argument #2 for method _ZStplIcSt11char_traitsIcESaIcEENSt7__cxx1112basic_stringIT_T0_T1_EEOS8_PKS5_
00000000004018a2         mov        rdi, rax                                    ; argument #1 for method _ZStplIcSt11char_traitsIcESaIcEENSt7__cxx1112basic_stringIT_T0_T1_EEOS8_PKS5_
00000000004018a5         call       _ZStplIcSt11char_traitsIcESaIcEENSt7__cxx1112basic_stringIT_T0_T1_EEOS8_PKS5_ ; std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > std::operator+<char, std::char_traits<char>, std::allocator<char> >(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&&, char const*)
00000000004018aa         lea        rdx, qword [rbp+var_80]
00000000004018ae         lea        rax, qword [rbp+var_C0]
00000000004018b5         mov        rsi, rdx
00000000004018b8         mov        rdi, rax
00000000004018bb         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEpLERKS4_
00000000004018c0         lea        rax, qword [rbp+var_80]
00000000004018c4         mov        rdi, rax
00000000004018c7         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEED1Ev
00000000004018cc         lea        rax, qword [rbp+var_A0]
00000000004018d3         mov        rdi, rax
00000000004018d6         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEED1Ev
00000000004018db         jmp        loc_40197c

loc_4018e0:
00000000004018e0         mov        eax, dword [rbp+var_F4]                     ; CODE XREF=main+225
00000000004018e6         add        eax, 0x1
00000000004018e9         movsxd     rdx, eax
00000000004018ec         lea        rax, qword [rbp+var_E0]
00000000004018f3         mov        rsi, rdx
00000000004018f6         mov        rdi, rax
00000000004018f9         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm
00000000004018fe         movzx      eax, byte [rax]
0000000000401901         movsx      ebx, al
0000000000401904         mov        eax, dword [rbp+var_F4]
000000000040190a         movsxd     rdx, eax
000000000040190d         lea        rax, qword [rbp+var_E0]
0000000000401914         mov        rsi, rdx
0000000000401917         mov        rdi, rax
000000000040191a         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm
000000000040191f         movzx      eax, byte [rax]
0000000000401922         movsx      eax, al
0000000000401925         lea        edx, dword [rbx+rax]
0000000000401928         lea        rax, qword [rbp+var_60]
000000000040192c         mov        esi, edx
000000000040192e         mov        rdi, rax                                    ; argument #1 for method _ZNSt7__cxx119to_stringEi
0000000000401931         call       _ZNSt7__cxx119to_stringEi                   ; std::__cxx11::to_string(int)
0000000000401936         lea        rax, qword [rbp+var_40]
000000000040193a         lea        rcx, qword [rbp+var_60]
000000000040193e         mov        edx, 0x402268
0000000000401943         mov        rsi, rcx                                    ; argument #2 for method _ZStplIcSt11char_traitsIcESaIcEENSt7__cxx1112basic_stringIT_T0_T1_EEOS8_PKS5_
0000000000401946         mov        rdi, rax                                    ; argument #1 for method _ZStplIcSt11char_traitsIcESaIcEENSt7__cxx1112basic_stringIT_T0_T1_EEOS8_PKS5_
0000000000401949         call       _ZStplIcSt11char_traitsIcESaIcEENSt7__cxx1112basic_stringIT_T0_T1_EEOS8_PKS5_ ; std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > std::operator+<char, std::char_traits<char>, std::allocator<char> >(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&&, char const*)
000000000040194e         lea        rdx, qword [rbp+var_40]
0000000000401952         lea        rax, qword [rbp+var_C0]
0000000000401959         mov        rsi, rdx
000000000040195c         mov        rdi, rax
000000000040195f         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEpLERKS4_
0000000000401964         lea        rax, qword [rbp+var_40]
0000000000401968         mov        rdi, rax
000000000040196b         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEED1Ev
0000000000401970         lea        rax, qword [rbp+var_60]
0000000000401974         mov        rdi, rax
0000000000401977         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEED1Ev

loc_40197c:
000000000040197c         add        dword [rbp+var_F4], 0x1                     ; CODE XREF=main+357
0000000000401983         jmp        loc_40180d

loc_401988:
0000000000401988         mov        dword [rbp+var_F0], 0x0
```

Here, the program loops through each character in the string and basically does the following operation:

*For each character, it adds the next character and writes the ascii representation of that integer to the flag buffer followed by a comma*

Here is a diagram to help explain what it does:

![](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/raw/ec055096672b3ca26df1a600ae572486e5db4bc9/2017/PACTF_2017/problems/boole/Decider/encodeDiagram.png)

We can check this by breaking and examining the flag buffer in gdb:

```
$ gdb -q decider
Reading symbols from decider...(no debugging symbols found)...done.
(gdb) b *0x401988
Breakpoint 1 at 0x401988
(gdb) r
Starting program: /home/ubuntu/pactf/decider

Breakpoint 1, 0x0000000000401988 in main ()
(gdb) x/x $rbp-0xc0
0x7fffffffe460:	0x00615c50
(gdb) x/s 0x00615c50
0x615c50:	"182,222,211,132,108,193,216,206,140,33,"
```

Alright, that is the string we expect, let's move on.

### 3. First pass XOR

```
					loc_401992:
0000000000401992         mov        eax, dword [rbp+var_F0]                     ; CODE XREF=main+646
0000000000401998         movsxd     rbx, eax
000000000040199b         lea        rax, qword [rbp+var_C0]
00000000004019a2         mov        rdi, rax
00000000004019a5         call       j__ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6lengthEv
00000000004019aa         cmp        rbx, rax
00000000004019ad         setb       al
00000000004019b0         test       al, al
00000000004019b2         je         loc_4019fe

00000000004019b4         mov        eax, dword [rbp+var_F0]
00000000004019ba         movsxd     rdx, eax
00000000004019bd         lea        rax, qword [rbp+var_C0]
00000000004019c4         mov        rsi, rdx
00000000004019c7         mov        rdi, rax
00000000004019ca         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm
00000000004019cf         mov        rbx, rax
00000000004019d2         mov        eax, dword [rbp+var_F0]
00000000004019d8         movsxd     rdx, eax
00000000004019db         lea        rax, qword [rbp+var_C0]
00000000004019e2         mov        rsi, rdx
00000000004019e5         mov        rdi, rax
00000000004019e8         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm
00000000004019ed         movzx      eax, byte [rax]
00000000004019f0         xor        eax, 0x61
00000000004019f3         mov        byte [rbx], al
00000000004019f5         add        dword [rbp+var_F0], 0x1
00000000004019fc         jmp        loc_401992
```

Here is the first XOR pass. We see a loop where each byte of the flag buffer is equal to: `byte XOR 0x61`. Let's inspect the flag buffer after this point as well:

```
$ gdb -q decider
Reading symbols from decider...(no debugging symbols found)...done.
(gdb) b *0x4019fe
Breakpoint 1 at 0x4019fe
(gdb) r
Starting program: /home/ubuntu/pactf/decider

Breakpoint 1, 0x00000000004019fe in main ()
(gdb) x/x $rbp-0xc0
0x7fffffffe460:	0x00615c50
(gdb) x/s 0x00615c50
0x615c50:	"PYSMSSSMSPPMPRSMPQYMPXRMSPWMSQWMPUQMRRM"
```

Alright, that string looks similar to the string we were provided. At this point you can actually solve the string we were given by reversing everything up to this point. However, I'll continue reversing the program to explain why we sometimes get different outputs.

### Second pass XOR

I won't embed assembly at this point because it can be summarized nicely. Basically, here we see a call to `time` and `srand` followed by `rand`. So we are generating a random number based on the time - therefore we can't really break the seed. The random number is then scaled down within the range of one byte.

Then, we see a second loop where we do multiple passes of the string and perform XOR a bunch of times with random values (however it is constant for each pass).

Remember that XOR is associative:

```python
(a XOR b) XOR c = a XOR (b XOR c)
```

So all these additional operations can be treated as a *single* XOR operation.

It is possible to brute force this space and find the values we expect from the first encoding scheme. Here is an example:

We'll use a random output obtained from the binary:

```python
a = "FOE[EEE[EFF[FDE[FGO[FND[EFA[EGA[FCG[DD["
for i in range(255):
	print(str(i) + ' ' + "".join([chr(ord(x) ^ i) for x in a]))
```

Here is part of the output:

```
...
114 4=7)777)744)467)45=)4<6)743)753)415)66)
115 5<6(666(655(576(54<(5=7(652(642(504(77(
116 2;1/111/122/201/23;/2:0/125/135/273/00/
117 3:0.000.033.310.32:.3;1.034.024.362.11.
118 093-333-300-023-019-082-307-317-051-22-
119 182,222,211,132,108,193,216,206,140,33,  
120 >7=#===#=>>#><=#>?7#>6<#=>9#=?9#>;?#<<#
121 ?6<"<<<"<??"?=<"?>6"?7="<?8"<>8"?:>"=="
122 <5?!???!?<<!<>?!<=5!<4>!?<;!?=;!<9=!>>!
123 =4> >>> >== =?> =<4 =5? >=: ><: =8< ??
...
```

Notice that when we use 119 as a key, we see the familiar encoding scheme:

```
182,222,211,132,108,193,216,206,140,33,
```

# Decoding the flag

We were given the following flag:

```
SPQMSQTMSQQMPXYMSPVMSSVMSQWMSQQMPWYMPVPMPWYMPRXMPRQMPWQMSQWMSSSMSQXMSPPMSRSMPYUMPYSMSPRMSSTMSRXMPPYM
```

We can use the method discussed previously to break the XOR key. In the output we see:

```
...
97 210,205,200,198,217,227,206,200,168,171,168,139,130,160,206,222,209,211,232,184,182,213,225,239,118,
...
```

Now that we have the intermediate value we can decode it. Since the last character of the flag is passed through directly to the flag buffer, we can work backwards to determine the rest of the flag:

```python
# encoded flag
a = "210,205,200,198,217,227,206,200,168,171,168,139,130,160,206,222,209,211,232,184,182,213,225,239,118"
a = a.split(',')
a = [int(x) for x in a]
a = a[::-1]

# output
o = []

# previous byte
p = 0

# decode
for i in range(len(a)):
	o.append(a[i] - p)
	p = (a[i] - p)

# reverse and print
o = o[::-1]
o = [chr(x) for x in o]

print("".join(o))
```

This prints:

```
$ python breakDecider.py
flag_ziecEfBI9ggwZyoImhyv
```

Flag: `flag_ziecEfBI9ggwZyoImhyv`
