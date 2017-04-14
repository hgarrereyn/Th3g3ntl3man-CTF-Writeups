import random

encflag = "BNZQ:2m8807395d9os2156v70qu84sy1w2i6e"

random.seed("random")
flag = ""
for c in encflag:
  if c.islower():
    #rotate number around alphabet a random amount
    flag += chr((ord(c)-ord('a')-random.randrange(0,26))%26 + ord('a'))
  elif c.isupper():
    flag += chr((ord(c)-ord('A')-random.randrange(0,26))%26 + ord('A'))
  elif c.isdigit():
    flag += chr((ord(c)-ord('0')-random.randrange(0,10))%10 + ord('0'))
  else:
    flag += c
print flag
