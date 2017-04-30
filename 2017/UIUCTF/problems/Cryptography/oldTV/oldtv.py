from binascii import hexlify
from fractions import gcd
import rsa

pub, priv = rsa.newkeys(2048)

with open('flag.txt') as f: flag = f.read()

signme = 1337

q = priv.q
p = priv.p
d = priv.d
e = priv.e
n = priv.n

# RSA signatures are way too slow I'm gonna go sanic

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

s1 = pow(signme, d % (p - 1), p)
s2 = pow(signme, d % (p - 1), q)
qinv = modinv(q, p)
h = (qinv * (s1 - s2)) % p
s = s2 + h * q

print "parameters:"
print e
print n
print "signed 1337 with"
print s
print "encrypted flag"
print hexlify(rsa.encrypt(flag, pub))
