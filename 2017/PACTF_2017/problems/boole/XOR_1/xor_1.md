
XOR 1 - 20 points
===

Writeup by poortho
------
Problem Statement:
My friend Miles sent me a secret message. He said he encoded it with an XOR cipher. Can you figure out what his message “KGZFK\qZFG]qA\qZFOZ” means?

Hint:

The key is only one digit long

------

Writeup
------
As the problem states, the text is encrypted using single-byte XOR. To solve this, we can simply write a program to brute force all possible keys.

```python
def sxor(s1,s2):    
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

s = "KGZFK\qZFG]qA\qZFOZ"
for x in range(128):
    print sxor(chr(x)*len(s),s)

```

Scrolling through the output, we see the flag.

Flag
------

`either_this_or_that`
