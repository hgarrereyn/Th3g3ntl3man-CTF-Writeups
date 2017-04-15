# Raw2Hex
#### Writeup by hgarrereyn
* **Reverse Engineering**
* *20 points*
* Description: This program just prints a flag in raw form. All we need to do is convert the output to hex and we have it! CLI yourself to /problems/963285fb64e4c5f7a31b5a601c704f99 and turn that Raw2Hex!

# Solution

In this directory, we find a binary `raw2hex` that prints out the raw flag:

```
$ ./raw2hex
The flag is:??~Y?މJ?B>?
```

We need to convert this output to it's hexadecimal representation and submit that as the flag.

We can solve this with another python one-liner:

```
$ ./raw2hex | python -c "a = raw_input(); print(''.join([hex(ord(x))[2:] for x in a[12:]]))"
e519e7aa7e593fde891bd24aaa423ea4
```

# Building the python one-liner

```python
a = raw_input() # gets the output of raw2hex
a[12:]	# the output without the leading 'The flag is:'
[ord(x) for x in a[12:]] # creates a list of the integer values for each character in the flag
[hex(ord(x))[2:] for x in a[12:]] # convert those integers to hex values and strip off '0x'
''.join([hex(ord(x))[2:] for x in a[12:]]) # turn the list back into a string with no gaps
print(''.join([hex(ord(x))[2:] for x in a[12:]])) # Print it out
```

Flag: `e519e7aa7e593fde891bd24aaa423ea4`
