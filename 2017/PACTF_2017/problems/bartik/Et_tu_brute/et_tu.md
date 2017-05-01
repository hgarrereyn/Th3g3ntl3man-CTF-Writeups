
Et tu, Brute? - 5 points
===

Writeup by poortho
------
Problem Statement:
I found a message from Julius. Can you get the flag? Huk aopz pz aol mshn: clup_cpkp_cpjp_TqTfUK

Hint:

Look up what a Caesar cipher is. Can you make sense of the encrypted text above? Once you do, enter the ‘flag’ in the text box below and check if you’re right!

------

Writeup
------
As the problem says, the message is encrypted using a caesar cipher. We simply plug this in to an online tool such as [rot13.com](rot13.com) and check all the possible keys.

By doing this, we can obtain the plaintext and the flag: `And this is the flag: veni_vidi_vici_MjMyND`

Flag
------

`veni_vidi_vici_MjMyND`