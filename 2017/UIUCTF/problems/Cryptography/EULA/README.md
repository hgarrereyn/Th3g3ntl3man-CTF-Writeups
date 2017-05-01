# EULA - 400 points

#### Writeup by Valar_Dragon
* **Cryptography, RSA Key Forgery**
* 9 Solves

## Problem
nc challenge.uiuc.tf 11345

throwback to when the aztecs sacked mitlan
[eula.py](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/blob/4cd2aa69e6b21aa17fcd8d064d9658b1d7fe2430/2017/UIUCTF/problems/Cryptography/EULA/eula.py)

##Solution

This is one of those challenges where it looks we don't have enough to solve it. We see from the code that we have to forge a signature for the message `right below`, but we don't even know the modulus!

We know that:
* The modulus is 2048 bits
* The public exponent is 3
* The program uses python's RSA module.
* The program runs the latest version of said module as of 2015-07-29 (Almost 2 Years ago!!)

I started this after the challenge was already solved, so I knew that it was *solvable*. I tried for awhile to figure out a solution to this on my own, but I had no luck. Then I decided to use the hint that it was the latest version as of 2015. So I decided to google for past vulnerabilities on Python's RSA Module.

I first came across this:
https://nvd.nist.gov/vuln/detail/CVE-2016-1494
, a CVE on this python RSA module, for key signing! And it was released way after 2015. Looks like we're onto something!

And then I found https://blog.filippo.io/bleichenbacher-06-signature-forgery-in-python-rsa/
which details how to perform a bleichenbacher attack on the python RSA module! Essentially this attack gives us a solution that will forge a signature for ANY modulus, as long as we are know the bitsize! Really all I did was code what was described on that page. My code is in [solver.py]https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/blob/4cd2aa69e6b21aa17fcd8d064d9658b1d7fe2430/2017/UIUCTF/problems/Cryptography/EULA/solver.py)

I'll describe the bleichenbacher attack anyway in my own words, because its cool.

Recall that verifying an RSA signature is raising a given input, to a public exponent mod N, and seeing if gives you what you expected.

So an RSA signature in the python RSA module is supposed to be:

`00 01 FF FF FF ... FF 00 ASN.1 Hash`

ASN.1 is a bytestring which is essentially a lookup table for the hashtype, and the hash is just that type of hash over the message. There are enough FF bytes to make the signature have the same length as the modulus.

But what the python RSA module was checking for was that the signature
* ended in `00 ASN.1 HASH`
* Started with `00 01`
* There is not a single byte in between that start and end which is null bytes.

Since those intermittent bytes can be anything, we just need to find a suffix that when cubed gives us the ending. Then for the prefix, we can just take the cubed root of some number that meets `00 01 XX XX XX ... XX`, and verify that it has no null bytes. Then we can just replace the last few bytes of that with the suffix, since the suffix cubed will always give the same ending, regardless of the digits to the left of it.

Lets number the bits from the right, where the 0th bit is the Least significant bit. To find the suffix you use the property the Nth bit will not affect the 0th through N-1th bit.

There is a really good graphical explanation here: https://blog.filippo.io/bleichenbacher-06-signature-forgery-in-python-rsa/

A key thing is you can't forge it if the hash % 2 == 0, unless hash%8==0.

So we couldn't use MD5, but we have 6 hash types to choose from, so we're good on that front since we could just use SHA-256

Running my Solver.py to get a valid forgery, we can get send it to the server to get the flag.

```
~/Code/CTF/UIUCTF/EULA $ nc challenge.uiuc.tf 11345
have you read the terms and conditions? [y/N] y
OK, sign right below 2b1f3650277dc17957420b4eb10e3ced50257dc81500f51b973d4017d2fc3120005a62a0d4fa6114f4a9bddb94224f7d491eb57f2ac6773916261697612c7ec51fae2165fa6aaad0bffc049808bbcea472355c27df
verifying rsa signature 2b1f3650277dc17957420b4eb10e3ced50257dc81500f51b973d4017d2fc3120005a62a0d4fa6114f4a9bddb94224f7d491eb57f2ac6773916261697612c7ec51fae2165fa6aaad0bffc049808bbcea472355c27df for message "right below"...
flag{it_was_all_good_just_a_key_ago}
```

This is yet another reason you shouldn't use low exponents.
We had to take the cube root for e=3, and we could solve it because the cube root was longer than the cube of the forged suffix. If that suffix^e was longer than the eth root of the fake prefix, then we couldn't solve it with this method. (Or alternatively if python-rsa had checked it properly, there would be no issue)
