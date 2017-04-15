# A Thing Called the Stack
#### Writeup by hgarrereyn
* **Reverse Engineering**
* *60 points*
* Description: A friend was stacking dinner plates, and handed you this, saying something about a "stack". Can you find the difference between the value of esp at the end of the code, and the location of the saved return address? Assume a 32 bit system. Submit the answer as a hexidecimal number, with no extraneous 0s. For example, the decimal number 2015 would be submitted as 0x7df, not 0x000007df.

# Links

Here is the file we were given:

**assembly.s**
```asm
foo:
    pushl %ebp
    mov %esp, %ebp
    pushl %edi
    pushl %esi
    pushl %ebx
    sub $0x12c, %esp
    movl $0x1, (%esp)
    movl $0x2, 0x4(%esp)
    movl $0x3, 0x8(%esp)
    movl $0x4, 0xc(%esp)

```

# Solution

In order to understand this file, we must first understand how x86 calling convention works.

When a subroutine wants to call another part of code (and wants that code to jump back), it uses the `call` instruction. This instruction is like a special version of `jmp`. In addition to modifying the instruction pointer, it also pushes the return value onto the stack. Therefore, when the subroutine is finished and it has created and consumed its stack frame, it can simply call `ret` which will pop the return address off the stack and jump to it.

Assuming that `foo` has been called by another subroutine (eg. `bar`), the stack frame at the start of `foo` should look like this:

```
Higher addresses	| param 3 	|
					| param 2 	|
					| param 1 	|
Lower addresses		| ret addr 	|	<= %esp
```

Parameters (if there were any) should have been pushed onto the stack in reverse order before the `call` instruction. Also notice that the stack is growing from *higher addresses* to *lower addresses*.

Now, we can step through `foo` and imagine what the stack frame will look like. First, we see that foo sets up it's own stack frame (which is a standard thing for subroutines to do).

```asm
pushl %ebp
mov %esp, %ebp
```

After these instructions, our stack frame looks like this:

```
Higher addresses	| param 3 	|
					| param 2 	|
					| param 1 	|
					| ret addr 	|
					| saved ebp | 	<= %esp
```

Now we encounter three `push` instructions:

```asm
pushl %edi
pushl %esi
pushl %ebx
```

The stack frame now looks like this:

```
Higher addresses	| param 3 	|
					| param 2 	|
					| param 1 	|
					| ret addr 	|
					| saved ebp |
					| %edi		|
					| %esi		|
					| %ebx		|	<= %esp
```

In the description, the problem tells us to assume we are using a 32 bit system. That means that each value on the stack takes up exactly 4 bytes. Therefore, every time we push something onto the stack, we *decrement esp by 0x4*. Therefore, at this moment, the difference between the saved return address and the value of `esp` is `4 (pushes) * 4 (bytes per push) = 0xf`.

Now we execute a `sub` command:

```asm
sub $0x12c, %esp
```

The stack frame looks like this:

```
Higher addresses	| param 3 	|
					| param 2 	|
					| param 1 	|
					| ret addr 	|
					| saved ebp |
					| %edi		|
					| %esi		|
					| %ebx		|
					...
					< 0x12b omitted >
					...
					|			|	<= %esp
```

The difference between `esp` and the location of the saved return address is now: `0xf + 0x12c = 0x13c` because we have just moved the stack pointer even further away from saved return address (remember stack grows towards lower addresses).

The next 4 `mov` instructions do not actually modify `esp`. The parenthesis around `%esp` means that it is being dereferenced. Instead of moving values into the `%esp` register, the `mov` commands are writing values to the place that `%esp` is pointing to (on the stack).

Therefore, the final offset doesn't change and we can submit it as the flag.

Flag: `0x13c`
