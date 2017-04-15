# Hex2Raw
#### Writeup by hgarrereyn
* **Reverse Engineering**
* *20 points*
* Description: This program requires some unprintable characters as input... But how do you print unprintable characters? CLI yourself to `/problems/c69bcda4ca5a28fd9d18790fc763db73` and turn that Hex2Raw!

# Solution

Login to the shell and traverse to the given directory. You will find three files:

```
$ ls
flag  hex2raw  input

$ ./hex2raw
Give me this in raw form (0x41 -> 'A'):
416f1c7918f83a4f1922d86df5e78348

You gave me:
```

The `hex2raw` binary asks you to convert a hex code into ascii (and then hopefully it will print the flag).

We can convert this hexcode and pipe it to `hex2raw` with the python function `.decode('hex')`

```
hgarrereyn@shell-web:/problems/c69bcda4ca5a28fd9d18790fc763db73$ python -c "print('416f1c7918f83a4f1922d86df5e78348'.decode('hex'))" | ./hex2raw

Give me this in raw form (0x41 -> 'A'):
416f1c7918f83a4f1922d86df5e78348

You gave me:
416f1c7918f83a4f1922d86df5e78348
Yay! That's what I wanted! Here be the flag:
1d2411efe307f5ac07bd28bbabb5769e
```

Flag: `1d2411efe307f5ac07bd28bbabb5769e`
