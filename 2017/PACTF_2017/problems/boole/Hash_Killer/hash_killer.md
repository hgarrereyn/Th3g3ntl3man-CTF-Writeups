
Hash Killer - 60 points
===

Writeup by poortho
------
Problem Statement:
Qu’est que c’est?

We were clearing out the old server and came across a really weird [file](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/raw/20050537d284122523a4309013f5e68f20ac3380/2017/PACTF_2017/problems/boole/Hash_Killer/hashes.txt)…

Hint:

Did someone say MD5? And that last line seems different from the rest…

------

Writeup
------
Looking at the txt file, there seems to be several hashes along with a base64 encoded string.

To decrypt the hashes, we can go to [Hashkiller](https://hashkiller.co.uk/md5-decrypter.aspx) as the problem title suggests. We can simply enter the hashes, and we get:
```
c7218260ef2b966ab0454e07c55cf4e9 MD5 : oh
639bae9ac6b3e1a84cebb7b403297b79 MD5 : you
27e76ef6b60400df7c6bedfb807191d6 MD5 : wish
0d149b90e7394297301c90191ae775f0 MD5 : it
2b016d90959eda144d600e4f870c30ba MD5 : were
9e925e9341b490bfd3b4c4ca3b0c1ef2 MD5 : this
48bb6e862e54f2a795ffc4e541caed4d MD5 : easy
d1457b72c3fb323a2671125aef3eab5d MD5 : ?
73cf0e388971ee4ec34e8daedd0d36cc MD5 : sorry
01b6e20344b68835c5ed1ddedf20d531 MD5 : to
e1686078d1b60d351da5a87543a2a663 MD5 : let
639bae9ac6b3e1a84cebb7b403297b79 MD5 : you
74e8333ad11685ff3bdae589c8f6e34d MD5 : down
37598dad8f8805ce708ba8c4f67ce367 MD5 : but
9e925e9341b490bfd3b4c4ca3b0c1ef2 MD5 : this
a51e47f646375ab6bf5dd2c42d3e6181 MD5 : rabbit
de97e75e5b4604526a2afaed5f5439d7 MD5 : hole
89fe7b5ca56cdee4e750f4eb3ab12fbb MD5 : goes
c376109ef8d15c46a24936b7d0e0b560 MD5 : deeper
9033e0e305f247c0c3c80d0c7848c8b3 MD5 : !
8fc42c6ddf9966db3b09e84365034357 MD5 : the
c47d187067c6cf953245f128b5fde62a MD5 : word
424149e499a7cb738810dc0e537c8490 MD5 : 'AES'
0800fc577294c34e0b28ad2839435945 MD5 : hash
a2a551a6458a8de22446cc76d639a9e9 MD5 : is
8fc42c6ddf9966db3b09e84365034357 MD5 : the
3c6e0b8a9c15224a8228b9a98ca1531d MD5 : key
97bc592b27a9ada2d9a4bb418ed0ebed MD5 : now
9a2d8ce3ffdcdf2123bddd94d79ef200 MD5 : decrypt
ab86a1e1ef70dff97959067b723c5c24 MD5 : me
b078ffd28db767c502ac367053f6e0ac MD5 : START
```

This tells us two things:
1. The base64 encoded string is encrypted using AES
2. The AES string is encrypted with the md5 hash of `AES`

For some reason, python code on the internet to decrypting AES simply would not work. I ended up using [this tool](http://aes.online-domain-tools.com/) to get the flag.

First, we can convert the base64 to hex using python:
```python
print "mJRKaaMSR1atUGs0kOkAJP3dty9tjCvXKMzWDHtZdRQ=".decode('base64').encode('hex')
```

Doing so gives us `98944a69a3124756ad506b3490e90024fdddb72f6d8c2bd728ccd60c7b597514` as our ciphertext.

Afterwards, we can take the md5 hash of the string `AES` and get `76b7593457e2ab50befe2dcd63cf388f`.

Plugging these into the website, we get the flag!

Note: The password for the AES was the hex of the md5 hash in lowercase... not really a good idea, especially because others may have only thought to try uppercase or that we had to use the raw of the md5 hash.

Flag
------

`flag{w3_l0v3_3ncrypt10n}`
