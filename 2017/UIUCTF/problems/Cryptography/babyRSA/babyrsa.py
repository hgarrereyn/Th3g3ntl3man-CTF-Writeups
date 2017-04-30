#! /usr/bin/env python2

from Crypto.PublicKey import RSA

key = RSA.generate(4096, e=5)
msg = "welcome to uiuctf!\nyour super secret flag is: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
m = int(msg.encode("hex"), 16)
c = pow(m, key.e, key.n)

f = open("babyrsa.txt", "w")
print >> f, "n = {}".format(key.n)
print >> f, "e = {}".format(key.e)
print >> f, "c = {}".format(c)
