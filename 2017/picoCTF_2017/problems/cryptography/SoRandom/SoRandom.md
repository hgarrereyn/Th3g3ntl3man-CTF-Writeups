# SoRandom
#### Writeup by Valar_Dragon
* **Cryptography**
* *75 points*
* We found [sorandom.py](sorandom.py) running at shell2017.picoctf.com:33123. It seems to be outputting the flag but randomizing all the characters first. Is there anyway to get back the original flag?

Lets start by looking at sorandom.py!
```python
import random,string

flag = "FLAG:"+open("flag", "r").read()[:-1]
encflag = ""
random.seed("random")
for c in flag:
  if c.islower():
    #rotate number around alphabet a random amount
    encflag += chr((ord(c)-ord('a')+random.randrange(0,26))%26 + ord('a'))
  elif c.isupper():
    encflag += chr((ord(c)-ord('A')+random.randrange(0,26))%26 + ord('A'))
  elif c.isdigit():
    encflag += chr((ord(c)-ord('0')+random.randrange(0,10))%10 + ord('0'))
  else:
    encflag += c
print "Unguessably Randomized Flag: "+encflag
```

We are actually given the seed for the RNG, so the sequence of random numbers isn't actually random. So we just need to reverse the encflag, by subtracting the random number instead of adding it. Connecting to the server a couple times, you see that the encflag being returned is the same everytime, further evidence of the same seed being used.
```
$ nc shell2017.picoctf.com 33123
Unguessably Randomized Flag: BNZQ:2m8807395d9os2156v70qu84sy1w2i6e
```

So making a solver that repeats the code of sorandom.py, except with subtracting the random number, and using encflag instead of flag, we get:
```
$ python solver.py
FLAG:9b6098160b2ca5139c83fe29fd7c9e5d
```

Which is our flag!
