# MIPS
#### Writeup by hgarrereyn
* **Reverse Engineering**
* *140 points*
* Description: The modern renaissance man knows of many things, ranging from cyber security, to architecture. Can you prove that you're more than just a computer whiz? mips. Enter the flag as a hexadecimal number, prefixed by 0x

# Overview

This program accepts a single 4-byte integer as an input and prints either `Not quite! Keep trying.` or `Good job! Submit your input value as the flag.`.

There is exactly one integer that works.

# Solution

To solve this, I first had to read up on MIPS (I actually printed out some pages from wikepedia so I could reference the opcodes).

One new thing for me was the concept of a "branch delay slot". Basically, this is an extra instruction that comes after a jump and is executed even if the jump succeeds. For example, look at this line in the assembly code:

```mips
b       $L3
addiu   $3,$3,-13
```

The `addiu` instruction will execute before the branch instruction.

My approach was to work at the code from two sides:
1. Figure out what conditions have to be met at the end in order to print the success message
2. Figure out how the input was broken down and stored

Then as I went, I took notes next to the assembly code and tried to simplify the conditional expressions.

Early on, I figured out that the integer input was broken down into 4 individual bytes that were operated on independently for a significant portion of the program.

One thing I noticed happening was shift and add - which is a way to multiply two numbers. Take for example the following python code:

```python
byte = 34

a = (byte << 3) + (byte << 4) + (byte << 6)
```

This kind of thing occured quite a bit in the MIPS assembly. Now, in order to simplify it, remember that lshift is simply multiply by 2. So that expression becomes:

```python
a = (byte * 2**3) + (byte * 2**4) + (byte * 2**6)
```

or

```python
a = byte * 88
```

I used this technique of simplifying down many lines of assembly in order to come up with the following two conditions that had to be met to have the right flag:

```python
(16,777,215)(b0) + (-12,517,375)(b1) + (b3) - 1922105344 + 18176 == 0
b2 == (b3 * 2) + 3
```
where `b0` is the most significant byte of the input and `b3` is the least.

Now, we need integer solutions to this equation so I wrote a simple python force to check possibilites (note: it checks 2^16 solutions which is significantly reduced from the 2^32 possible solution space)

[**mipsSolver.py**]()

```python
# By Harrison Green <hgarrereyn>

def a(b0,b1,b3):
	return (16777215 * b0) + (-12517375 * b1) + b3 - 1922105344

for i in range(0,256):
	for j in range(0,256):
		v = a(i,j,0)

		if abs(v) < 18176 + 256:
			b0 = i
			b1 = j
			b3 = -v
			b2 = (b3 * 2) + 3

			val = (b0 << 24) + (b1 << 16) + (b2 << 8) + b3

			print('Bytes: ' + str([b0,b1,b2,b3]))

			print('Decimal: ' + str(val))

			print('Hex: ' + hex(val))
```

Running this script gives:

```
$ python mipsSolver.py
Bytes: [175, 81, 191, 94]
Decimal: 2941370206
Hex: 0xaf51bf5e
```

We can verify that this solution is correct by entering the decimal number into a MIPS emulator.

Then we submit the hex value as the flag.

Flag: `0xaf51bf5e`
