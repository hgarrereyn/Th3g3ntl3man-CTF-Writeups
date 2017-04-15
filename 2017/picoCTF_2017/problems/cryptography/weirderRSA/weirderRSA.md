## WeirderRSA - 175 (Cryptography)

#### Writeup by pwang00 (Sanguinius)



### Problem

Another message encrypted with RSA. It looks like some parameters are missing. Can you still decrypt it?

[Message](https://webshell2017.picoctf.com/static/7b8498694279da845b09e10587e432b1/clue.txt)

### Hint

Is there some way to create a multiple of p given the values you have?

Fermat's Little Theorem may be helpful.

## Solution

### Overview

Perform a partial key exposure attack on the given parameters

### Details

We are given a text file with the following parameters:

```
e = 65537

n = 211767290324398254371868231687152625271180645754760945403088952020394972457469805823582174761387551992017650132806887143281743839388543576204324782920306260516024555364515883886110655807724459040458316068890447499547881914042520229001396317762404169572753359966034696955079260396682467936073461651616640916909
dp = 10169576291048744120030378521334130877372575619400406464442859732399651284965479823750811638854185900836535026290910663113961810650660236370395359445734425

c = 42601238135749247354464266278794915846396919141313024662374579479712190675096500801203662531952565488623964806890491567595603873371264777262418933107257283084704170577649264745811855833366655322107229755242767948773320530979935167331115009578064779877494691384747024161661024803331738931358534779829183671004
```

It appears that we are given several parameters for Chinese Remainder Theorem \(CRT\) decryption of RSA.  RSA-CRT decryption is identical to standard RSA decryption, except that instead of using a single private key $d$, we use

$$d_p = d \pmod{p-1}$$

$$d_q = d \pmod{q-1}$$

If used correctly, this allows for speedup when compared to normal RSA decryption, since two smaller modular exponentiations are performed with significantly smaller exponents.

Unfortunately, we are not given $$d_q$$. However, since we are given $$d_p$$, we are essentially given an entire portion of the private key - effectively compromising the security of the cryptosystem.

Howgrave-Graham showed that as long as we know the lower half of the Least Significant Bits (LSBs) of $$d_p$$, and $$e$$ is of size *poly(log(N))*, we can obtain the factorization of the modulus in polynomial time.  

We know from RSA-CRT that $$ed_p = 1 \pmod{p-1}$$

Rearranging the equation: we arrive at

$$ed_p - 1 = 0\pmod{p-1}$$, meaning that $$ed_p - 1$$ evenly divides $$p-1$$.

This can be rewritten as:

$$ed_p - 1 = k(p-1)$$, where $$k\in\mathbb{N}$$ and $$k < e$$, since $$k(p-1)$$ is a multiple of  $$ed_p - 1$$

Solving for $$p$$, we obtain $$p = \frac{ed_p - 1 + k}{k}$$

Since $$e = 65537$$, it is completely feasible to try every $$k$$ in the range of $$e$$ until we obtain a value of $$k$$ such that $$\frac{N}{p} = \lfloor{}\frac{N}{p}\rfloor{}$$, in which case we know that we have obtained the prime factor $$q$$ and thus the factorization of $$N$$.

I wrote the following python script to perform the task:

    import binascii
    import string

    e = 65537
    N = 211767290324398254371868231687152625271180645754760945403088952020394972457469805823582174761387551992017650132806887143281743839388543576204324782920306260516024555364515883886110655807724459040458316068890447499547881914042520229001396317762404169572753359966034696955079260396682467936073461651616640916909
    dp = 10169576291048744120030378521334130877372575619400406464442859732399651284965479823750811638854185900836535026290910663113961810650660236370395359445734425

    c = 42601238135749247354464266278794915846396919141313024662374579479712190675096500801203662531952565488623964806890491567595603873371264777262418933107257283084704170577649264745811855833366655322107229755242767948773320530979935167331115009578064779877494691384747024161661024803331738931358534779829183671004

    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(a, m):
        g, x, y = egcd(a, m)
        if g != 1:
            raise 'Modular inverse does not exist.'
        else:
            return x % m

    def factorize():
        for k in range(2,e):
            p = (e * dp - 1 + k) // k #Solves for p
            if N % p == 0:
                return p
        return -1

    p = factorize()
    q = N // p

    phi = (p - 1) * (q - 1)
    d = modinv(e,phi)
    print(binascii.unhexlify(hex(pow(c,d,N))[2:]))

    >>>b'flag{wow_leaking_dp_breaks_rsa?_32697643574}

Which returns the flag!

## Flag

    flag{wow_leaking_dp_breaks_rsa?_32697643574}

## Resources

https://www.iacr.org/archive/crypto2003/27290027/27290027.pdf
