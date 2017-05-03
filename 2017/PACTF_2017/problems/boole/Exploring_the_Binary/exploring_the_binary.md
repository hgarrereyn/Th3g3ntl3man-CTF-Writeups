
Exploring the Binary!!! - 10 points
===

Writeup by poortho
------
Problem Statement:
Binary 1

Why doesn’t [this file](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/raw/20050537d284122523a4309013f5e68f20ac3380/2017/PACTF_2017/problems/boole/Exploring_the_Binary/a.out) print!! Did I forget to put in the print statement when I compiled?

Hint:

Well running it does nothing, maybe try looking inside?

------

Writeup
------
As with all very low-point value reversing problems, we can simply run strings on the file and get the flag:
```
$ strings a.out | grep "flag"
flag_1297831859
```

Flag
------

`flag_1297831859`
