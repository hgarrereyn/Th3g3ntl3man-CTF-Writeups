## Encrypted Shell - 190 points

#### Writeup by Valar_Dragon



### Problem

[This service](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/blob/master/2017/picoCTF_2017/problems/cryptography/Encrypted_Shell/dhshell.py) gives a shell, but it's password protected! We were able intercept [this encrypted traffic](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/blob/master/2017/picoCTF_2017/problems/cryptography/Encrypted_Shell/traffic.pcap)
which may contain a successful password authentication. Can you get shell access and read the contents of flag.txt?
The service is running at shell2017.picoctf.com:40209.


## Solution

### Overview

Use Pollards Kangaroo Algorithm on the data in the pcap to recover the server password, then just connect normally through nc, enter the password, and cat for the flag!

### Details

So if you dive into the source code behind the service, you see that it does indeed use  the Diffie Hellman Key Exchange, as the name implies. They read p and g from a file, and then randomly generate a on range(1, 2**46).

That seems pretty secure, no way we're ever gonna be able to brute 2**46!

The server asks for B (the parameter of our choosing), then the remainder of the communication with the server must be symmetrically encrypted with this diffie hellman key.
The encryption, decryption, and padding methods are all provided in [dhshell.py](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/blob/master/2017/picoCTF_2017/problems/cryptography/Encrypted_Shell/dhshell.py), so we don't have to worry about that. The messages are essentially based on AES, so the padding is secure.

After we give it B, it asks us for the password. (Well it doesn't ask, you have to read src to figure that out.) If you enter the password correctly, your command gets run over the shell. Otherwhise you get booted out.
Interestingly, the admins actually had left several errors in the file, which if we run:
```
$ nc shell2017.picoctf.com 40209
Welcome to the
______ _   _   _____ _          _ _
|  _  \ | | | /  ___| |        | | |
| | | | |_| | \ `--.| |__   ___| | |
| | | |  _  |  `--. \ '_ \ / _ \ | |
| |/ /| | | | /\__/ / | | |  __/ | |
|___/ \_| |_/ \____/|_| |_|\___|_|_|

Parameters:
p = 174807157365465092731323561678522236549173502913317875393564963123330281052524687450754910240009920154525635325209526987433833785499384204819179549544106498491589834195860008906875039418684191252537604123129659746721614402346449135195832955793815709136053198207712511838753919608894095907732099313139446299843
g = 41899070570517490692126143234857256603477072005476801644745865627893958675820606802876173648371028044404957307185876963051595214534530501331532626624926034521316281025445575243636197258111995884364277423716373007329751928366973332463469104730271236078593527144954324116802080620822212777139186990364810367977
A = 156439341998271326670854407853012976764262288786929988839529709826828422232670472310365037800284072340235486706283005338468448237653712979317842659987697497127703110446780267034878733794922311404471812801624206593707502453597072975694923902719171702681870307700853226866506301755446619246056034103194097113506
Please supply B: 1059
ffffffffff  
Traceback (most recent call last):
  File "/problems/f2f49fa60b38c0c21571653080db7a4b/dhshell.py", line 68, in <module>
    pw = read_encrypted(KEY)
  File "/problems/f2f49fa60b38c0c21571653080db7a4b/dhshell.py",
  -SNIP-
ValueError: IV must be 16 bytes long
```

We get the location of the problems directory, which is on the same server we have ssh access to! Unfortunately permissions were setup correctly, so looks like we're gonna have to get the shared key from this pcap!

If we open Traffic.pcap, and follow the TCP Stream, we get the DH public keys for the session.

![TCP Stream](https://raw.githubusercontent.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/master/2017/picoCTF_2017/problems/cryptography/Encrypted_Shell/TCP_Stream.png)

So the general approach that we need to take is fairly clear.
We need to crack A or B in the given TCP Stream, and then generate that shared secret key to decode the password.

Then we need to reconnect ourselves, ls, and then cat flag.txt!

So how do we crack this Diffie Hellman exchange?
Well this is really the sort of problem that if you've heard of it before, only takes a few minutes, but if you've never heard of it can take a few hours.
We fell in the latter category. Everyone has to start somewhere!

The parameter $$ p $$ was a safe prime, so Pohlig-Hellman was out of the picture.
The square root of p was still a massive number, so baby step giant step wasn't really feasible.
Eventually, after digging into the different methods to solve the Discrete Log Problem, we came across [Pollard's Kangaroo Algorithm](https://en.wikipedia.org/wiki/Pollard%27s_kangaroo_algorithm)

Given a range of possible values for the public exponent, it would compute the DLP in
$$ O(\sqrt{range}) $$
Looking back at our parameters, a was generated with an upperbound of $$ 2^{46} $$, which means the DLP is $$ 2^{23} $$ which is definitely doable!

Even better sage has an inbuilt function for this, so we just have to put it all into sage!

```python
#Get a from following sage code:
sage:
p = 174807157365465092731323561678522236549173502913317875393564963123330281052524687450754910240009920154525635325209526987433833785499384204819179549544106498491589834195860008906875039418684191252537604123129659746721614402346449135195832955793815709136053198207712511838753919608894095907732099313139446299843
g = 41899070570517490692126143234857256603477072005476801644745865627893958675820606802876173648371028044404957307185876963051595214534530501331532626624926034521316281025445575243636197258111995884364277423716373007329751928366973332463469104730271236078593527144954324116802080620822212777139186990364810367977
A = 60599224471338675280892530751916349778515159413752423808328059701102187627870714718035966693602191072973114841123646111608872779841184094624255525186079109811898831481367089940015561846391171130215542875940992971840860585330764274682844976540740482087538338803018712681621346835893113300860496747212230173641
k = GF(p)
Afield = k(A)
gfield = k(g)
discrete_log_lambda(Afield,gfield,(1,2**46))
33657892424673
```

So that gives us a!!
Now we can decode that entire session which in the pcap!
This is coded in getPassword.py

```
$ python getPassword.py
ThisIsMySecurePasswordPleaseGiveMeAShell
****TRAILINGCHARS
echo "Does this shell work?"****TRAILINGCHARS
Does this shell work?
****TRAILINGCHARS
exit****TRAILINGCHARS
****TRAILINGCHARS
```
The reason I added Trailing chars when outputting is because the admins were devious. The password actually had a trailing '\n' in it!

Now we can just connect to the server, then send and decrypt our messages to get the flag! I wrote up the client-side in in `myEnd.py`.
You enter the message to encrypt in command line, and paste that into nc session.
Prefix any messages to decrypt with a "g". So I start the NC Session, replace the A in myEnd.py, and then encode ls, decode the response, send cat flag.txt, and decode that reponse for the flag.

Sadly the flag is a bunch of random text, nothing exciting.
`ac72f7354114b5b0909ab78812eb58ca`

This is genuinely a really easy problem, if you have heard of Pollard's Kangaroo Algorithm!
