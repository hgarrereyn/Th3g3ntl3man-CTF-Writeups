# MegaEncryption (TM) - 40 points

#### Writeup by Valar_Dragon

## Problem

**Personal Advancement of Cuil Therory Foundation**

The Personal Advancement of Cuil Therory Foundation (PACTF) left a message for [Tony](https://en.wikipedia.org/wiki/User:Tony_Tan), but they used MegaEncryption (TM) to encrypt it. What did they say? Should we be worried? It seems like they used some sort of public medium to send the message…

## Solution

Someone left an encrypted message for wikipedia user Tony, and they used a public medium to do so. The perfect place to do this would be Tony's talk page, so lets check the history of the talk page!

Navigate here:
https://en.wikipedia.org/w/index.php?title=User_talk:Tony_Tan&action=history

![User_talk_Tony_Tan_Revision_history_Wikipedia.png](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/blob/f9f6dafda99766c212875c1aff6e15c4a74df596/2017/PACTF_2017/problems/bartik/Mega_Encryption/User_talk_Tony_Tan_Revision_history_Wikipedia.png?raw=true)

What revision to look at is rather obvious.

We see:
```
#Super Secret Mega Encrypted Message

Hey Tony, I've got a super secret message for you! I had to use MegaEncryption (TM) to encrypt it, though. I speak on behalf of the Personal Advancement of Cuil Therory Foundation (PACTF). See my MegaEncrypted message below.

[20KB Base64 string that is too big to fit here, see megaEncrypted.txt]
```

This is clearly a base64 encoded message, because its all printable with no special characters, and ends in two equal signs. But its massive. So lets put it in a file called [megaEncrypted.txt](https://raw.githubusercontent.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/f9f6dafda99766c212875c1aff6e15c4a74df596/2017/PACTF_2017/problems/bartik/Mega_Encryption/megaEncrypted.txt)

If we do:
``` bash
$ cat megaEncrypted.txt | base64 -d
```
we get another massive base64 message. We can keep on piping more base64's until we get the message at the end.

```
$ cat megaEncrypted.txt | base64 -d |
 base64 -d | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d| base64 -d | base64 -d| base64 -d | base64 -d | base64 -d | base64 -d
Oh my goodness! It's gotten so bad. The cuils are rising... they want to outlaw encryption... I'd rate their world +200 Cuils! At least I have MegaEncryption (TM) to keep me safe. the_cuil_is_too_much_to_handle
```
If you scroll all the way to the right, you see the flag:
`the_cuil_is_too_much_to_handle`

Challenge could more accurately be called MegaEncoded :P
