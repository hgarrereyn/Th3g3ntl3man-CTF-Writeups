# DLP

* **Cryptography, DLP**
* *158 points*
* You should solve a DLP challenge, but how? Of course , you don't expect us to give you a regular and boring DLP problem!
`nc 146.185.143.84 28416`

![nc Server](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/blob/master/2017/ASIS_CTF_Quals_2017/problems/DLP/DLP.png?raw=true)

Let's look at the function they used to encrypt this:

``` python
def encrypt(nbit, msg):
    msg = bytes_to_long(msg)
    p = getPrime(nbit)
    q = getPrime(nbit)
    n = p*q
    s = getPrime(4)
    enc = pow(n+1, msg, n**(s+1))
    return n, enc
```

The DLP we need to solve is then
$$ (n+1)^{msg} \equiv enc (\bmod n^{s+1})$$

_s_ is a 4 bit prime, so its either 11 or 13

If we look at the public key, we see that n is 1024 bits long, and essentially can't really be factored efficiently, so that rules out the Pohlig Hellman attack.

However, theres a trick we can do to simplify this! Recall the binomial expansion:

$$ (a+b)^m = a^m + ma^{m-1}b + {m \choose 2} a^{m-2}b^2 + ... +{m \choose m-2} a^{2}b^{m-2} +{m \choose m-1} ab^{m-1} + b^m $$

Also
$${m \choose m-1} = m$$
 look at [Pascal's Triangle](https://en.wikipedia.org/wiki/Pascal%27s_triangle) if you need to jog your memory of this :)

So in our case we have:

$$ (n+1)^m = n^m + mn^{m-1} + {m \choose 2} n^{m-2} + ... +{m \choose m-2} n^{2} + m*n + 1 \equiv enc \  (\bmod n^{s+1})$$

Any equation that is true mod x, is also true mod any factor of x! n is obviously a factor of our modulus. Therefore
$$enc \bmod n \equiv 1$$
and
$$enc \bmod n^2 \equiv msg*n + 1$$
If we rearrange the latter, we get
$$msg = (enc - 1 \bmod n^2) / n$$

If we do that, we get: `ASIS{Congratz_You_are_Discrete_Logarithm_Problem_Solver!!!}`

*Disclaimer: I did not solve this during the CTF, but it was an awesome challenge, so I made a writeup anyway*
