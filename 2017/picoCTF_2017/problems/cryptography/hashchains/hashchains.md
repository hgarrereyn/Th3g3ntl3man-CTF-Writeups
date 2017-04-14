# Hashchains
#### Writeup by Valar_Dragon

* **Cryptography, Hashchains**
* *90 points*
* Description: We found a service hiding a flag! It seems to be using some kind of MD5 Hash Chain authentication to identify who is allowed to see the flag. Maybe there is a flaw you can exploit? Connect to it at shell2017.picoctf.com:38130!

The key to this problem is that hashchains are easy to compute, so a simple brute force can solve the problem.

A hashchain with seed `a` is really just a chain of hashes:

$$ a \Rightarrow hash(a) \Rightarrow hash(hash(a)) \Rightarrow... $$

In this case, our hashing function is MD5, which is rather easy to compute.

First lets connect to the service, and see what we need to do for this problem.
```
*******************************************
***            FlagKeeper 1.1           ***
*  now with HASHCHAIN AUTHENTICATION! XD  *
*******************************************

Would you like to register(r) or get flag(f)?
r/f?
r
Hello new user! Your ID is now 7724 and your assigned hashchain seed is 454cecc4829279e64d624cd8a8c9ddf1
Please validate your new ID by sending the hash before this one in your hashchain (it will hash to the one I give you):
f80b3b5ee838f2d78e461c57ee2b7c03
```

The first thing to notice is that our hashchain seed is just the MD5 of our ID. So really the seed is our ID. Then we just need to setup a brute force, where we keep on taking iterations of our hashchain, until we get our goal! Doing that bruteforce, gives us `3e800ed70a66cff2a0fe067e65063a79`, and entering that gives us a friendly "Yep! That's it! You're validated"


Well that was easy, lets go get the flag now!
```
*******************************************
***            FlagKeeper 1.1           ***
*  now with HASHCHAIN AUTHENTICATION! XD  *
*******************************************

Would you like to register(r) or get flag(f)?
r/f?
f
This flag only for user 58
Please authenticate as user 58
7707549aa0961667e6d64d308c4b82f1
Next token?
```

Looks like we are supposed to use the same verification process as in registering. Looks like this time they don't give us the seed, good thing we worked out that our seed is really our ID number.
Using the exact same script as previously, we get `08af8baa8fe0ce4836f09fb597bc96b3`

Entering that into our netcat session, we are welcomed into the server with "Hello user 58! Here's the flag: 739045aa5b814fba124d5899a2d7d78b"

So we have our flag!
