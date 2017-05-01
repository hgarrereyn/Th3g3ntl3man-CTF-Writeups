# Commonplace

#### Writeup by Valar_Dragon

* **Cryptography**
* *200 points*
* The communication between WikiLeaks and their informant is protected asymmetrically.
Fortunately for you, they each have a little something in common.
[input](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/blob/7f2daab679cd091cf45d0e375eb2a17a2a3a5f37/2017/tamuCTF/problems/commonplace/input)

So we have two messages, (presumably the same plaintext), encrypted with two separate public exponents, under the same modulus.
What can we do with this?
Lets denote what we have as:

$$ c_1,c_2,e_1,e_2,N $$

We know that
$$ GCD(e_1,e_2)==1$$
which means that there exists some $$s_1, s_2$$ such that

$$s_1e_1 + s_2e_2 = 1 $$
This is known as the bezout identity, exactly the parameters extended euclidean algorithm solves for!

Now, lets see if we can use this finding

$${C_1}^{s_1}{C_2}^{s_2} \equiv ({M}^{e_1})^{s_1}*({M}^{e_2})^{s_2} \equiv M^{e_1s_1 + e_2s_2} (mod \ N)$$

Now notice the exponent is our bezout identity, so we really are left with

$$M^{e_1s_1 + e_2s_2} \equiv M (mod \ N)$$

which is just our message!

So now we just have to program this. Obtaining $$s_1,s_2$$ is trivial with the extended euclidean algorithm. So we just modpow and multiply as normal, with the caveat that a negative power is really just the absolute value of that power, but of the multiplicative modular inverse of the base.

Writing this in solver.py, we get:

`gigem{c0mm0nly_knOwn_AS__bb90200cdb4ac55f}`

###### Backstory
So I actually helped the admin fix this problem.
Originally, the problem had one modulus, two public exponents, 65537, and 65538, and two ciphertexts. Since 65538 is an invalid public exponent, my assumption was it was the same message (from chal name), and that you just multiply modular inverse of the ciphertext for the 65537th power against the other ciphertext, so that the exponent would add to 1, and would leave you the message!

It turns out however, that there were several layers of errors on the admins end, that I helped fix. Essentially the attack was supposed to be a common modulus attack, where the same message was encrypted with two different public exponents, same modulus.
Except two different messages were being encrypted at the time.
There were also a few additional complications.

To help fix the problem, I ended up wroting a solver for how problem should've been, showed to admin, then helped fix generation code, then problem got updated and we solved it.
