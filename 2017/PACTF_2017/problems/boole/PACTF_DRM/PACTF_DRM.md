# PACTF DRM
#### Writeup by hgarrereyn
* **Reverse Engineering**
* *40 points*
* The flag is in encrypted.txt. You also get the decoder software. Unfortunately, the software is protected by its own custom DRM(Digital Rights Management). …And it’s very protective about its things.

# Solution

We've been given some decoding software as well as the encrypted flag.

Running the program we see that it does not want to cooperate.

```
$ ./drm
Sorry buddy. But I'm not gonna decrypt it for you.
```

Let's look at the assembly to see what functions we are provided:

### `main`

```asm
					main:
000000000040274b         push       rbp                                         ; DATA XREF=_start+29
000000000040274c         mov        rbp, rsp
000000000040274f         sub        rsp, 0x40
0000000000402753         mov        rax, qword [fs:0x28]
000000000040275c         mov        qword [rbp+var_8], rax
0000000000402760         xor        eax, eax
0000000000402762         mov        dword [flagLength], 0x10
000000000040276c         mov        esi, 0x403b50                               ; "Sorry buddy. But I'm not gonna decrypt it for you."
0000000000402771         mov        edi, 0x605220
0000000000402776         call       j__ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
000000000040277b         mov        esi, 0x401fe0
0000000000402780         mov        rdi, rax
0000000000402783         call       j__ZNSolsEPFRSoS_E
0000000000402788         mov        eax, 0x1
000000000040278d         mov        rdx, qword [rbp+var_8]
0000000000402791         xor        rdx, qword [fs:0x28]
000000000040279a         je         loc_4027a1

000000000040279c         call       j___stack_chk_fail
                        ; endp

                     loc_4027a1:
00000000004027a1         leave                                                  ; CODE XREF=main+79
00000000004027a2         ret
```

Ok, clearly main is not going to call any useful functions. Let's see what else there is.

I found a subroutine named `decrypt` that might be useful:

### `decrypt`

```asm
					_Z7decryptNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE:        // decrypt(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)
000000000040270e         push       rbp
000000000040270f         mov        rbp, rsp
0000000000402712         sub        rsp, 0x50
0000000000402716         mov        qword [rbp+var_48], rdi
000000000040271a         mov        qword [rbp+var_50], rsi
000000000040271e         mov        rax, qword [fs:0x28]
0000000000402727         mov        qword [rbp+var_8], rax
000000000040272b         xor        eax, eax

					loc_40272d:
000000000040272d         mov        esi, 0x403b08                               ; "CAN'T MAKE ME DECRYPT IT. NOT GONNA DO IT! YOU AREN'T MY CREATOR!", CODE XREF=_Z7decryptNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE+59
0000000000402732         mov        edi, 0x605220
0000000000402737         call       j__ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
000000000040273c         mov        esi, 0x401fe0
0000000000402741         mov        rdi, rax
0000000000402744         call       j__ZNSolsEPFRSoS_E
0000000000402749         jmp        loc_40272d
```

Nope, unfortunately, it just looks like it prints:

```
CAN'T MAKE ME DECRYPT IT. NOT GONNA DO IT! YOU AREN'T MY CREATOR!
```

How about if we we look at the `encrypt` function and try to reverse engineer it?

### `encrypt`

```asm
					loc_4021f8:
00000000004021f8         mov        eax, dword [flagLength]                     ; CODE XREF=_Z7encryptNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE+233
00000000004021fe         cmp        dword [rbp+var_264], eax
0000000000402204         jge        loc_4022a4

000000000040220a         mov        eax, dword [rbp+var_264]
0000000000402210         movsxd     rdx, eax
0000000000402213         mov        rax, qword [rbp+var_280]
000000000040221a         mov        rsi, rdx
000000000040221d         mov        rdi, rax
0000000000402220         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm
0000000000402225         movzx      eax, byte [rax]
0000000000402228         movsx      eax, al
000000000040222b         add        eax, eax
000000000040222d         xor        eax, 0x2e
0000000000402230         mov        edx, eax
0000000000402232         lea        rax, qword [rbp+var_260]
0000000000402239         mov        esi, edx
000000000040223b         mov        rdi, rax                                    ; argument #1 for method _ZNSt7__cxx119to_stringEi
000000000040223e         call       _ZNSt7__cxx119to_stringEi                   ; std::__cxx11::to_string(int)
0000000000402243         lea        rax, qword [rbp+var_240]
000000000040224a         lea        rcx, qword [rbp+var_260]
0000000000402251         mov        edx, 0x403ae1
0000000000402256         mov        rsi, rcx
0000000000402259         mov        rdi, rax
000000000040225c         call       _ZStplIcSt11char_traitsIcESaIcEENSt7__cxx1112basic_stringIT_T0_T1_EEOS8_PKS5_ ; std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > std::operator+<char, std::char_traits<char>, std::allocator<char> >(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&&, char const*)
0000000000402261         lea        rdx, qword [rbp+var_240]
0000000000402268         mov        rax, qword [rbp+var_278]
000000000040226f         mov        rsi, rdx
0000000000402272         mov        rdi, rax
0000000000402275         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEpLERKS4_
000000000040227a         lea        rax, qword [rbp+var_240]
0000000000402281         mov        rdi, rax
0000000000402284         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEED1Ev
0000000000402289         lea        rax, qword [rbp+var_260]
0000000000402290         mov        rdi, rax
0000000000402293         call       j__ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEED1Ev
0000000000402298         add        dword [rbp+var_264], 0x1
000000000040229f         jmp        loc_4021f8
```

This is subsection of the `encrypt` function that appears to be doing the encryption. We see a loop over the flag's length and some cryptic c++ function calls.

The key part is the following:

```asm
0000000000402225         movzx      eax, byte [rax]
0000000000402228         movsx      eax, al
000000000040222b         add        eax, eax
000000000040222d         xor        eax, 0x2e
0000000000402230         mov        edx, eax
```

This part of the subroutine takes a byte from the flag, adds it to itself and XORs it with `0x2e`. Knowing this, the flag is encoded per character as: `(2 * byte) XOR 0x2e`.

Since we have the encrypted flag, we can reverse this function to: `(byte XOR 0x2e) / 2`. Let's try this in python:

```python
>>> a = "244 72 144 182 188 184 164 136 144 230 236 198 144 166 138 180"
>>> a = a.split(' ')
>>> "".join([chr((int(x) ^ 0x2e) / 2) for x in a])
'm3_LIKES_dat_DRM'
```

Flag: `m3_LIKES_dat_DRM`
