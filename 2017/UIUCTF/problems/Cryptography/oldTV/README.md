# Old TV - 200 points

#### Writeup by Valar_Dragon
* **Cryptography, RSA Signature**
* 7 Solves (We were the frst solve!)

## Problem
gotta go fast

[oldtv.py](eula.py) [out.txt](out.txt)

##Solution

We're given the RSA signature of the message `1337`, (it being raised to private exponent d), the method used to do this, the public key, and a ciphertext to decrypt.

First lets just verify the signature!
Lets call the signature `s`
For an RSA signature, `pow(s,e,n) = m = 1337`, but instead in our case,
`pow(s,e,n) = 12552144872630883274714072545559463757828118071630665151722772056407721299934616162810530304997659992415564308701396117393025354645107530976713649239409451803997740359880122405939605548778021703199551273864163090482150066695631817414629720018307875632681097178104630114937573873294907023222567946816504903037260500658928600670497051598898376986773062001031938767195249333798228769916200946963769451909639742894282759235781105274175124872151644261876601757211440162264594875362591406072507719407672461649360911713429957298410768243018558682972729448246596003808359170080421648418783136047933670607778691976167563837725`

So this definitely isn't a valid signature! Lets look into whats going on in the code.

The writer was *trying* to use the CRT method to speedup the calculation, but instead they made an error:

```python
s1 = pow(signme, d % (p - 1), p)
s2 = pow(signme, d % (p - 1), q)
```

they messed up s2! copy/paste fail! It should've been `d % (q-1)`.

So now we have to figure out what we end up. The way CRT is done for the CRT-RSA speedup isn't the standard method of doing CRT, so I wasn't sure if it uses some hack for just RSA, or if it is a general method.

In hindsight, there are easier ways to verify that it is a general method, but I decided to derive the formula used.

We want to find a $$M$$ such that
1) $$ M \equiv m_1 \mod p $$

2) $$ M \equiv m_2 \mod q $$

Lets start with 2 being true. That means

$$ M = m_2 + hq $$

Applying that to 1, that means that:
$$ m_2 + hq \equiv m_1 \mod p $$

if we treated this as a normal equation and tried to solve for h, we'd first subtract both sides by $$m_2$$, then multiply both sides by $$\frac{1}{q}$$.

We can still do that in modular arithmetic, but instead of dividing by q, you multiply by modular multiplicative inverse of q. So:

$$ h = q^{-1}(m_1 - m_2) \mod p $$

So lines 35-37 really are the normal CRT!!

In our case for the challenge, they are taking the CRT of:
$$ m^{d \mod (p-1)} \mod p $$

$$ m^{d \mod (p-1)} \mod q $$

which would just be:

$$ m^{d \mod (p-1)} \mod N $$

So our signature, `s` is really just $$s= m^{d \mod (p-1)} \mod N $$ You can verify this by testing this with your own RSA key.

Now recall the definition of d:

$$ ed \equiv 1 \mod (p-1)(q-1) $$

if a modular equation is true mod X, it will also be true mod the factors of X.

So $$ed \equiv 1 \mod (p-1)$$

$$s^e \equiv m^{e(d \mod (p-1))} \mod N $$

The exponent is thus equivalent to 1 mod (p-1). Thus if we took the whole equation mod p instead of mod N we would get:

$$s^e \equiv m^{ed \mod (p-1)} = m^{(1 \mod (p-1))} \mod p $$

Which by Fermat's Little theorem is just m!

So $$ s^e = m + xp $$ if we take away the modular reduction.

$$ s^e - m = xp $$
We know another number which has p as a factor, N. So we can get p via GCD.
So $$p = GCD(s^e - m, N)$$

From there on its standard RSA for the flag!
```python
def main():
    e = 65537
    n = 18604062125510571031471750649821316329679075240425215155565854406809609668335654053956581181954590620902738575301840213122192524051208433461229187907016997447442571285108109128232900783308909475021812467308548398111895347558651286259631740349426896657319783170302728838343220396488616780511168826294004371666849527520273722614881089052945223370388126979539564867809681914897680522296481279349571443843378935124793042177857000433266432982960332119281263048730048547498134410661972444056093841057496584878791672081540003288714250151610555939149231061629657881570676337865434594411572171750122440981346430244089440952567
    s = 12626455418792952924024493013198098863512212246301282894118807005086832684489543287165894064859469025233806305193892189559421764939495917348639365119950426589182135875711093564051730704657842999676564205070064606256132658912124853451762683834028889637219143921647861439076750823378709406152722488707110077984370053893449731808240684680979671504757064703764328159125242166255082176828015391850248753018273523440027270913493592693734458075992742191195882811209889628438061441870649244037708043706068407190276646564212746198947056532105881136757836974357801862311991843532484468835666420055033931014325969526594149593232
    m = 1337
    flag = "5ac8379545f36bfd435952e122fd0780f3045e9c897b4681b606e8f0b82c5879c09d208d7111032acf5dc058dc5a4fa3ad2acc0588db728a6564c72f566f9f853ec26d439541886844b967e1d1ce9cff30a74b4a5651ed41cd3c274a66ee962ed9ebc7c4f9f4cb21a29998c7201eb6983da3f8bcb45f8a347cd3f8472e7bb89ae47c3e3e22327c8b48e3216275b5a7d0a6ed02d95a8902cae72adb64bc13add8ff909ff3bb017c740a2772f82b7822638b28b5f5b637975698e93e8b280994baed710e4b9d292550bcd672bcd7f7bce58ee695e1c64b8439f2a7e303e8cb2142948950101ae3361433c5f8d858527c7cca1d562c89321b06c8b846b9571fb576"
    p = gcd(pow(s,e)-m,n)
    q = n//p
    totn = (p-1)*(q-1)
    d = modinv(e,totn)
    flag = pow(int(flag,16),d,n)
    flag = hex(flag)[2:]
    if(len(flag) % 2 == 1):
        flag = '0'+ flag
    print(binascii.unhexlify(flag)
```
And after a bit of time spent computing that massive power, you get:

```
b'\x02,u\x9fM;\x81/\x99g\xf9\xb9\x89\xb0\xd0\xdd\x05\x18ep\x9c\xff\xabQ<\xc1x\x89U\xab\xcf\xcdu\xa2\x18\xf9\xf5\x0br\xa8|\x15\x14g\xaf\x1c\xac\xbe\x9d\xba\xb3\r\x91\x14!6\x86\xb6\xe3p$0&\xef\xb9Z\x06\xc2p^\x1fR\xc0\xa6Eq\xe5%\xfab\xc3\xd5\xf0\xceH0f\\\xa3Z\xcfue6\x84D\x88[\xc6`H\x99\xb0\x96\xa9\xc4\xbb2\xd7,m\xae\x8f\x8fScbl\xfd\xc0K\xa7\xf6>\xfb\x08\x95\xde\xb6:\xe2\xb55\x1c\x80u:\x93\xc0K+\xed\xfex\x8e\xb3\x12\x0c\xdce\xa6\x91r\xba\x82\x1a\xe3\x93\x18\xa5\xed\xebB\x89\x17\xc9\x08\x8b?x\xc8,\xa1>u\xba\x99\xb6M\x8c\xcc\xadLK\x802v\x87|*2\x8e\x97\xb5\x1e\xf7jB\x98D\xc2\xd0\x17 \xd9\xc9\xd3]L\xefG\x9e\xccm\xf1\x93e\n0\xbf\xd4\x17\xd3\xd8.\xa1B\xfb\xea\x9c\x00flag{lower_latency_tho}\n'
```

`flag{lower_latency_tho}`
