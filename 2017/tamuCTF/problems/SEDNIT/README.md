# SEDNIT

#### Writeup by Valar_Dragon

* **Reversing**
* *200 points*
* This program has a hidden functionality. Can you figure out what it is?
[3638e844ab2f7844](3638e844ab2f7844)

We are given an executable, but I didn't have the necessary libraries installed to run it.
So instead, I opened it up in atom, to see if there was anything that looked suspicious, as multiple stego problems were simply looking for base64 strings in the file in this CTF.

And in atom I see several suspiciously long base64 strings. I try to copy them into gedit so I can decode, them, but essentially it wouldn't copy. Taking a look in bless hex editors, there were tons of null bytes inbetween the characters inside of the file.

To fix this, I just did `cat 3638e844ab2f7844 | tr -d '\0' > noNulls`

Now we can just grab those 3 base64 strings and decode!

The first message gives us a RSA Public key
The second message gives us a RSA private key:
```
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCpYlZB7i44GkqIfqOorpAN0eJ/2RhPLgHqSGojSQmiJHXzSwNL
SOm2+0B4lbnqZmlKSVGwMvvmDxHfsdFFu3ZfZrcvx+Dh+ThFViDxQaWoWy7wSfVc
WzPjUZQ1Boifgm1pNt7GWLiSaiYnPHuOismvcSPRBlFfdu03/HxROsGdqQIDAQAB
AoGBAJSFhm7vIxXMb9g5etV4oxWLGNjTig47oDBG6NIhw9GpuMbo2m2T9GKe8owJ
dWiD/gTGP1uJiPjT8+86Yu6LDqHuATyYI6EG/xZ9VJFtH7fNnGvrEeSF5DuINRmk
cOHeuU+zRiwseljv9cn2+7UP8PioZ6xVExPhWFHDDyGNHWsRAkEAtqD8YrPUzWgG
y1TlDmUISkmzSRJAlcucLN5A+TG1bNkdpoDkDMp1oAssSjiLXdkVh3Fu/cfPWluQ
iDeDtPP9PQJBAO1vKF9FsxhTyBN0cqewa8J9DK3bmpNxQvMLfOCGhbn0cEmTIHPl
pFGvxPH6ZcbvqbwmCZLlNqfWMk6LlpagAN0CQAyK7+qDeUkGLPlIAldDvxcDCsoo
88CV9ErslL/IlzI7kxq9XWw3d26fddI/Ies3HpBnzPym/WmyQjHoxiXmX+0CQASL
CfS4urKOd9eXdNIsmANCrUluWEjV8/f+kkchi9GBEdz2ibpt/HTrrhMLPYNO9qp4
99nttNwFRzUlip4bNakCQHXelxW2kGmqOSZsSWKjof5txWVhvWDzjDfMZcwgd/Sl
H2V49nqBQF/J6hAtd4J/JW8WxTZfjZs24NMTqi6a0ao=
-----END RSA PRIVATE KEY-----
```
and the final message gives us a ciphertext!

So we use asn1parse to get the factors and modulus from the  private key, and decode our ciphertext straightforwardly!
Using the code in [decode.py](decode.py), we get:

`gigem{feels_g00d_2b_a_pIrate__04654a034d5ae22a}`

The flag probably makes way more sense if we could run the program!

Lesson: Always try opening files in both atom and bless. I never would've noticed the base64 in bless with the 100's of null bytes inbetween characters.
