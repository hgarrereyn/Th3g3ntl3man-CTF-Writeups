# Forest
#### Writeup by hgarrereyn
* **Reverse Engineering**
* *200 points*
* Description: I was wandering the forest and found a file. It came with some string

# Files

**String**
```
DLLDLDLLLLLDLLLLRLDLLDLDLLLRRDLLLLRDLLLLLDLLRLRRRDLLLDLLLDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLLRLDLLDLLRLRRDLLLDLLRLRRRDLLRDLLLLLDLLLRLDLLDLLRLRRDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLRDLLRLRRDLLLDLLLDLLRLRRRDLLLLLDLLLLRLDLLLRRLRRDDLLLRRDLLLRRLRDLLLRLDLRRDDLLLRLDLLLRRRDLLRLRRRDLRRLD
```

# Solution

We were provided with a binary and a string. My first move was to simply run the binary:

```
$ ./forest
You have the wrong number of arguments for this forest.
./forest [password] [string]
```

Ok, let's provide a random password with the given string:

```
$ ./forest password DLLDLDLLLLLDLLLLRLDLLDLDLLLRRDLLLLRDLLLLLDLLRLRRRDLLLDLLLDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLLRLDLLDLLRLRRDLLLDLLRLRRRDLLRDLLLLLDLLLRLDLLDLLRLRRDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLRDLLRLRRDLLLDLLLDLLRLRRRDLLLLLDLLLLRLDLLLRRLRRDDLLLRRDLLLRRLRDLLLRLDLRRDDLLLRLDLLLRRRDLLRLRRRDLRRLD
Nope.
```

Alright, it is clear now that we have to find the correct password for the given string.

### My Workflow

I run OSX so I prefer to use the Hopper disassembler for viewing binary files.
I run Ubuntu in VirtualBox and then ssh into it to run the binaries.
Then I can simply use `gdb` on the Ubuntu machine while referencing the code in Hopper (to set breakpoints etc...)

I also renamed locations and subroutines in Hopper to make it clearer what was going on. When I reference them in this writeup, I'll do: `nice_name(<address>)`.

### First look

![Image 1]()

I opened the binary in Hopper and peeked at the data section. It looks like we will see: `You did it! Submit the input as the flag` if we have the correct password. Also, I noticed an interesting string: `yuoteavpxqgrlsdhwfjkzi_cmbn` which doesn't look like a flag but might be used for something.

Next, I searched for references to the "You did it..." string:

Here is the function that prints it out:

![Image 2]()

Specifically, this line does the final check:

```
080487be         cmp        dword [ebp+var_10], 0x0
080487c2         je         wrong_password(0x080487d6)
```

So, if the two values are equal we have the wrong flag.

Let's walk through this subroutine from the start and see if we can find anything interesting.

```asm
			sub_8048748:
08048748         push       ebp
08048749         mov        ebp, esp
0804874b         push       ebx
0804874c         push       ecx
0804874d         sub        esp, 0x10
08048750         mov        ebx, ecx
08048752         mov        eax, dword [0x8049c0c]                              ; 0x8049c0c
08048757         sub        esp, 0xc
0804875a         push       eax                                                 ; argument #1 for method sub_80486f0
0804875b         call       sub_80486f0
08048760         add        esp, 0x10
08048763         mov        dword [ebp+var_C], eax
08048766         cmp        dword [ebx], 0x3
08048769         je         good_args(0x0804879b)
```

So we see that it sets up a stack frame, and then pushes a pointer of that weird string we found to the stack before calling `sub_80486f0` (subroutine at `0x80486f0`). Then it checks if we've supplied the right number of arguments and if we have, it branches to the `good_args` location.

I'll name this function `do_something_with_string(0x80486f0)`. Now none of the arguments passed to this subroutine were user-controlled so will skip over it for now and treat it as a static initialization routine.

If we have the right arguments, we branch to:

```asm
			good_args:
0804879b         mov        eax, dword [ebx+4]                                  ; CODE XREF=sub_8048748+33
0804879e         add        eax, 0x4
080487a1         mov        edx, dword [eax]
080487a3         mov        eax, dword [ebx+4]
080487a6         add        eax, 0x8
080487a9         mov        eax, dword [eax]
080487ab         sub        esp, 0x4
080487ae         push       edx                                                 ; argument #3 for method sub_804848b
080487af         push       eax                                                 ; argument #2 for method sub_804848b
080487b0         push       dword [ebp+var_C]                                   ; argument #1 for method sub_804848b
080487b3         call       sub_804848b
080487b8         add        esp, 0x10
080487bb         mov        dword [ebp+var_10], eax
080487be         cmp        dword [ebp+var_10], 0x0
080487c2         je         wrong_password(0x080487d6)
```

Here the program sets up three arguments to pass to `sub_804848b`. Then it stores the return value of this function and performs the check we saw earlier to print out the "You did it ..." string.

We'll call this function `check_password`. Let's see what the arguments being passed are. I find it easier to do dynamic analysis for this kind of thing instead of trying to calculate memory offsets in my head.

We'll set a breakpoint right before the call and examine the stack:

```
$ gdb -q forest
Reading symbols from forest...(no debugging symbols found)...done.
(gdb) b *0x080487b3
Breakpoint 1 at 0x80487b3
(gdb) r pass string
Starting program: /home/ubuntu/pico2017/forest pass string

Breakpoint 1, 0x080487b3 in ?? ()
(gdb) x/3x $esp
0xffffd480:	0x0804a008	0xffffd6a4	0xffffd69f
(gdb) x/s 0xffffd6a4
0xffffd6a4:	"string"
(gdb) x/s 0xffffd69f
0xffffd69f:	"pass"
```

So it is passing the following arguments:
1. A pointer to something on the heap
2. A pointer to the string
3. A pointer to the password

### `check_password(0x0804848b)`

Let's examine the `check_password` subroutine:

```asm
			check_password:
0804848b         push       ebp                                                 ; CODE XREF=sub_8048748+107
0804848c         mov        ebp, esp
0804848e         sub        esp, 0x18
08048491         cmp        dword [ebp+arg_0], 0x0
08048495         je         ret_zero

08048497         cmp        dword [ebp+arg_4], 0x0
0804849b         je         ret_zero

0804849d         cmp        dword [ebp+arg_8], 0x0
080484a1         jne        good_args

ret_zero:
080484a3         mov        eax, 0x0                                            ; CODE XREF=check_password+10, check_password+16
080484a8         jmp        ret(0x08048537)
```

This subroutine sets up a stack frame like usual. Then it checks if any of it's arguments are zero and if so, it returns zero. Otherwise, it continues at `good_args(0x080484ad)`.

### `good_args(0x080484ad)`

```asm
			good_args:
080484ad         mov        dword [ebp+var_C], 0x1                              ; CODE XREF=check_password+22
080484b4         mov        eax, dword [ebp+arg_4]
080484b7         mov        dword [ebp+var_10], eax
080484ba         mov        eax, dword [ebp+arg_8]
080484bd         mov        dword [ebp+var_14], eax
080484c0         jmp        check_loop_conditions(0x08048502)
```

Here we see a few variables getting initialized and then a jump to `check_loop_conditions(0x08048502)` where the function begins to behave like a `while` loop.

We also see three variables being initialized:
* `var_C` at `ebp - 0xC`
* `var_10` at `ebp - 0x10`
* `var_14` at `ebp - 0x14`

Let's do some dynamic analysis to see what these are set to:

```
$ gdb -q forest
Reading symbols from forest...(no debugging symbols found)...done.
(gdb) b *0x080484c0
Breakpoint 1 at 0x80484c0
(gdb) r pass string
Starting program: /home/ubuntu/pico2017/forest pass string

Breakpoint 1, 0x080484c0 in ?? ()
(gdb) x/wx $ebp-0xc
0xffffd46c:	0x00000001
(gdb) x/wx $ebp-0x10
0xffffd468:	0xffffd6a4
(gdb) x/s 0xffffd6a4
0xffffd6a4:	"string"
(gdb) x/wx $ebp-0x14
0xffffd464:	0xffffd69f
(gdb) x/s 0xffffd69f
0xffffd69f:	"pass"
```

One of the variables is initialized to `1` while the other two get the pointers to our two strings. We will name the first one `check` (this is a retroactive name, at the time I didn't know what this variable was used for).

So our new names are:

* `check` at `ebp - 0xC`
* `*string` at `ebp - 0x10`
* `*pass` at `ebp - 0x14`

### `check_loop_conditions(0x08048502)`

```asm
			check_loop_conditions:
08048502         mov        eax, dword [ebp+string]                             ; CODE XREF=check_password+53
08048505         movzx      eax, byte [eax]
08048508         test       al, al
0804850a         je         setup_return(0x08048516)

0804850c         mov        eax, dword [ebp+pass]
0804850f         movzx      eax, byte [eax]
08048512         test       al, al
08048514         jne        loop(0x080484c2)
```

Here, we see that two checks are performed. If either the string pointer or password pointer has reached a null byte (indicating the end of the string), we jump to `setup_return(0x08048516)`. Otherwise, we branch up to the body of the loop which will lead back to this routine.

### `setup_return(0x08048516)`

Let's see what we actually return from this function. Remember, if we return a non-zero value, we've solved the problem.

```asm
			setup_return:
08048516         mov        eax, dword [ebp+string]                             ; CODE XREF=check_password+127
08048519         movzx      eax, byte [eax]
0804851c         test       al, al
0804851e         sete       dl
08048521         mov        eax, dword [ebp+pass]
08048524         movzx      eax, byte [eax]
08048527         test       al, al
08048529         sete       al
0804852c         and        eax, edx
0804852e         movzx      eax, al
08048531         and        dword [ebp+check], eax
08048534         mov        eax, dword [ebp+check]

             ret:
08048537         leave                                                          ; CODE XREF=check_password+29
08048538         ret
```

So a few things happen here:
* We set `edx = 1` if the `string` pointer has reached the end of the string
* We set `eax = 1` if the `pass` pointer has reached the end of the string
* We then return the value: `(check & eax & edx)`

So in order to return a non-zero value:
* `check` must not be `0`
* Both the `string` and `pass` pointers must have reached the end of the string (and therefore will be pointing to null bytes)

Alright, let's look at the body of the loop and see how we can achieve this.

### `loop(0x080484c2)`

```asm
			loop:
080484c2         mov        eax, dword [ebp+pass]                               ; CODE XREF=check_password+137
080484c5         movzx      eax, byte [eax]
080484c8         movsx      eax, al
080484cb         sub        esp, 0x4
080484ce         push       eax                                                 ; argument #3 for method sub_8048539
080484cf         push       dword [ebp+string]                                  ; argument #2 for method sub_8048539
080484d2         push       dword [ebp+arg_0]                                   ; argument #1 for method sub_8048539
080484d5         call       check_pass_char(0x08048539)
080484da         add        esp, 0x10
080484dd         and        dword [ebp+check], eax
080484e0         add        dword [ebp+pass], 0x1
080484e4         jmp        consume_string

			inc_string:
080484e6         add        dword [ebp+string], 0x1                             ; CODE XREF=check_password+103, check_password+113

			consume_string:
080484ea         mov        eax, dword [ebp+string]                             ; CODE XREF=check_password+89
080484ed         movzx      eax, byte [eax]
080484f0         cmp        al, 0x4c ('L')
080484f2         je         inc_string

080484f4         mov        eax, dword [ebp+string]
080484f7         movzx      eax, byte [eax]
080484fa         cmp        al, 0x52 ('R')
080484fc         je         inc_string

080484fe         add        dword [ebp+string], 0x1
```

First, we see that `loop` calls a new subroutine with three arguments:
* The character that `pass` is pointing to
* The `string` pointer
* The pointer to the heap that we saw earlier

Then it takes the return value from the new subroutine (we'll call it `check_pass_char(0x08048539)`) and performs an `AND` operation with the `check` variable, storing the result in `check`. Ok, so if at any point this function returns zero, we have the wrong password.

Next, the `pass` string is incremented by one and we see that the `string` pointer is compared against two chars `L` and `R`. If it is pointing to either of these characters, it is incremented so that it is not.

Then right before we move out of the loop back to the conditions check, we see that `string` is incremented once more.

Recall that the string we were given was composed of three characters:
* `L`
* `R`
* `D`

So every loop, the `pass` pointer will increment by one and the `string` pointer will consume any `L` and `R` and end up pointing right after the next `D`.

Since both of these pointers must end up at the end of their respective strings, we know the length of `pass` must be the number of `D` characters in `string`.

For the string we were given, that is: `51` characters.

Now let's take a look at the `check_pass_char(0x08048539)` subroutine:

### `check_pass_char(0x08048539)`

```asm
check_pass_char:
08048539         push       ebp                                                 ; CODE XREF=check_password+74, check_pass_char+133, check_pass_char+182
0804853a         mov        ebp, esp
0804853c         sub        esp, 0x18
0804853f         mov        eax, dword [ebp+pass_char]
08048542         mov        byte [ebp+var_pass_char], al
08048545         cmp        dword [ebp+heap_pointer], 0x0
08048549         je         ret_zero____

0804854b         mov        eax, dword [ebp+string]
0804854e         movzx      eax, byte [eax]
08048551         test       al, al
08048553         jne        string_not_zero

             ret_zero____:
08048555         mov        eax, 0x0                                            ; CODE XREF=check_pass_char+16
0804855a         jmp        ret

             string_not_zero:
0804855f         mov        eax, dword [ebp+heap_pointer]                       ; CODE XREF=check_pass_char+26
08048562         movzx      eax, byte [eax+8]
08048566         cmp        al, byte [ebp+var_pass_char]
08048569         jne        heap_does_not_match_pass(0x08048593)

0804856b         mov        eax, dword [ebp+string]
0804856e         movzx      eax, byte [eax]
08048571         cmp        al, 0x44 ('D')
08048573         jne        ret_zero

08048579         mov        eax, dword [ebp+heap_pointer]
0804857c         movzx      eax, byte [eax+8]
08048580         cmp        al, byte [ebp+var_pass_char]
08048583         jne        ret_zero___

08048585         mov        eax, 0x1
0804858a         jmp        ret

             ret_zero___:
0804858c         mov        eax, 0x0                                            ; CODE XREF=check_pass_char+74
08048591         jmp        ret
```

A few things happen:
* The `pass` char argument is stored in a variable `var_pass_char`.
* If the heap pointer is null or if the string pointer has reached the end, the it returns zero.
* Otherwise, we jump to `string_not_zero(0x0804855f)` and see that it dereferences `heap_pointer + 8` as a char and compares it to the `pass_char`. If they are the same *and* the string pointer is pointing at a `D`, it returns 1.
* If `var_pass_char` and the dereferenced char do not match, we jump to `heap_does_not_match_pass(0x08048593)`.
* If they do match, but the string pointer is not at a `D`, return zero.

So, now we have some idea of what is on the heap. We know that there is a char pointer at `$heap_pointer + 8`:

```
Heap:
[8 bytes ??]	+0
[char]			+8
```

Let's see what happens if `var_pass_char` doesn't match the heap char:

```
			heap_does_not_match_pass:
08048593         mov        eax, dword [ebp+heap_pointer]                       ; CODE XREF=check_pass_char+48
08048596         movzx      eax, byte [eax+8]
0804859a         cmp        al, byte [ebp+var_pass_char]
0804859d         jle        pass_greater

			pass_less:
0804859f         mov        eax, dword [ebp+string]
080485a2         movzx      eax, byte [eax]
080485a5         cmp        al, 0x4c ('L')
080485a7         jne        ret_zero__

080485a9         movsx      edx, byte [ebp+var_pass_char]
080485ad         mov        eax, dword [ebp+string]
080485b0         lea        ecx, dword [eax+1]
080485b3         mov        eax, dword [ebp+heap_pointer]
080485b6         mov        eax, dword [eax]
080485b8         sub        esp, 0x4
080485bb         push       edx                                                 ; argument "pass_char" for method check_pass_char
080485bc         push       ecx                                                 ; argument "string" for method check_pass_char
080485bd         push       eax                                                 ; argument "heap_pointer" for method check_pass_char
080485be         call       check_pass_char
080485c3         add        esp, 0x10
080485c6         jmp        ret

			ret_zero__:
080485c8         mov        eax, 0x0                                            ; CODE XREF=check_pass_char+110
080485cd         jmp        ret

			pass_greater:
080485cf         mov        eax, dword [ebp+string]                             ; CODE XREF=check_pass_char+100
080485d2         movzx      eax, byte [eax]
080485d5         cmp        al, 0x52 ('R')
080485d7         jne        ret_zero_

080485d9         movsx      edx, byte [ebp+var_pass_char]
080485dd         mov        eax, dword [ebp+string]
080485e0         lea        ecx, dword [eax+1]
080485e3         mov        eax, dword [ebp+heap_pointer]
080485e6         mov        eax, dword [eax+4]
080485e9         sub        esp, 0x4
080485ec         push       edx                                                 ; argument "pass_char" for method check_pass_char
080485ed         push       ecx                                                 ; argument "string" for method check_pass_char
080485ee         push       eax                                                 ; argument "heap_pointer" for method check_pass_char
080485ef         call       check_pass_char
080485f4         add        esp, 0x10
080485f7         jmp        ret

			ret_zero_:
080485f9         mov        eax, 0x0                                            ; CODE XREF=check_pass_char+158
080485fe         jmp        ret

			ret_zero:
08048600         mov        eax, 0x0                                            ; CODE XREF=check_pass_char+58

			ret:
08048605         leave                                                          ; CODE XREF=check_pass_char+33, check_pass_char+81, check_pass_char+88, check_pass_char+141, check_pass_char+148, check_pass_char+190, check_pass_char+197
08048606         ret
```

First there is a second comparison between `var_pass_char` and the heap char. We branch to either `pass_less` or `pass_greater`.

If we branch to `pass_less` we see that it checks whether the string pointer is equal to `L` and then calls `check_pass_char` again with new arguments (dereferencing `heap_pointer`):

```
check_pass_char(*heap_pointer, string_pointer + 1, pass_char)
```

If we branch to `pass_greater` it does the same thing except it checks whether the string pointer is equal to `R` and then dereferences `heap_pointer + 4`:

```
check_pass_char(*(heap_pointer + 4), string_pointer + 1, pass_char)
```

So now we have a more complete picture of the heap structs:

```
Heap:
[* L]	+0
[* R]	+4
[char]	+8
```

We can make an educated guess on the struct as well:

```c
struct elem {
	struct elem* L;
	struct elem* R;
	char val;
};
```

So this means that we are simply traversing an (alphabetical) binary tree when we call `check_pass_char`. That must have been what the earlier subroutine was setting up.

### Decoding

We know now that each segment of the string ending in `D` corresponds to a position on the binary tree (and therefore a specific character). When the program runs it sets up the tree, then it compares each character in the password to each segment of the string. If everything matches, you have the right password.

Now let's try to decode the password from the given string. I'll set a breakpoint after the static initialization routine and do the dereferencing by hand in gdb. During the process, I'll also keep track of the parts of the tree I've seen so it goes quicker.

I won't show the whole process, but here is an example of getting the first two layers of the tree:

```
$ gdb -q forest
Reading symbols from forest...(no debugging symbols found)...done.
(gdb) b *0x08048760
Breakpoint 1 at 0x8048760
(gdb) r pass string
Starting program: /home/ubuntu/pico2017/forest pass string

Breakpoint 1, 0x08048760 in ?? ()
(gdb) x/c $eax + 8
0x804a010:	121 'y'
(gdb) x/wx $eax
0x804a008:	0x0804a018
(gdb) x/c 0x0804a018 + 8
0x804a020:	117 'u'
(gdb) x/wx $eax + 4
0x804a00c:	0x0804a148
(gdb) x/c 0x0804a148 + 8
0x804a150:	122 'z'
```

![layer1]()

When we split the string into segments, we get:

```
D
LLD
LD
LLLLLD
...
```

So for the first character, we don't traverse past the root element. Therefore, it is `y`.

Here is the final tree:

![]()

Then you simply go segment by segment and traverse the tree:

```
D           y
LLD         o
LD          u
LLLLLD      _
LLLLRLD     c
LLD         o
LD          u
LLLRRD      l
LLLLRD      d
LLLLLD      _
LLRLRRRD    s
LLLD        e
LLLD        e
LLLLLD      _
LLRD        t
LLLRRLD     h
LLLD        e
LLLLLD      _
LLLRLD      f
LLD         o
LLRLRRD     r
LLLD        e
LLRLRRRD    s
LLRD        t
LLLLLD      _
LLLRLD      f
LLD         o
LLRLRRD     r
LLLLLD      _
LLRD        t
LLLRRLD     h
LLLD        e
LLLLLD      _
LLRD        t
LLRLRRD     r
LLLD        e
LLLD        e
LLRLRRRD    s
LLLLLD      _
LLLLRLD     c
LLLRRLRRD   k
D           y
LLLRRD      l
LLLRRLRD    j
LLLRLD      f
LRRD        x
D           y
LLLRLD      f
LLLRRRD     m
LLRLRRRD    s
LRRLD       w
```

Flag: `you_could_see_the_forest_for_the_trees_ckyljfxyfmsw`
