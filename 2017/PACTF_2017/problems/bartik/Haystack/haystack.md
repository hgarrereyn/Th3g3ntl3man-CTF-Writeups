
What 3 Words - 60 points
===

Writeup by poortho
------
Problem Statement:
That’s a lot of data… but at least it’s signed! I’ll bet that at least one signature doesn’t match up, though. One of ‘em has a bit of cuil. It’ll be like finding a needle in a haystack…

[haystack.json](haystack.json)

Hint:

Yes, I know that the RSA key format doesn’t really matter in this scenario (considering there isn’t much of a format).

------

Writeup
------
We are given a massive json file, which we have to get the flag from. It seems to contain a huge array of data and signatures. At the bottom, it includes a RSA public key.

This problem is fairly straightforward - we have to create a script that verifies which data is properly signed, which will give us the flag.

First, however, we have to format the public key in a way such that python will recognize it.

To do this, we can use [this](https://superdry.apphb.com/tools/online-rsa-key-converter) online tool to convert the key to PEM format, which gives us:
```
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDEDtIRT57TJAfmub2RsIM32jdo
8ijsds/u1fpY6hwtkC01/LFJkNTXqSwvpaO5tp86o0SlzBHdF0WxPtsKqdc8F7kQ
uHm7hUTLX0zPGRdGCsy9q/PIGlVGAFTBSVXl+grmGGZuS1CHI13L/oulBGENQOxO
8r6D1RyPjt6z0BAndQIDAQAB
-----END PUBLIC KEY-----
```

Now, we can write a script to read the json and check every piece of data.

This is my code:
```python
import json
with open('haystack.json') as data_file:    
    data = json.load(data_file)

data = data["haystack"]

def verify_sign(public_key_loc, signature, data):
    '''
    Verifies with a public key from whom the data came that it was indeed 
    signed by their private key
    param: public_key_loc Path to public key
    param: signature String signature to be verified
    return: Boolean. True if the signature is valid; False otherwise. 
    '''
    from Crypto.PublicKey import RSA 
    from Crypto.Signature import PKCS1_v1_5 
    from Crypto.Hash import SHA256 
    from base64 import b64decode 
    pub_key = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC7/t8AXWyOuk9IULfWzA6HDPU5
1IKfAUCO1nxDlg8e2EiZX94cvaChFdl3UfpPNS/nxbJQwVlHaGHL070ETVJASzap
IgoS5HCchNkNyQPUJqGrviV8bs7+01Yq649TKD8xGdQ7nD39y+tfVnkfTmTSwiwT
lJiw4PEJ1RCw+PbwMQIDAQAB
-----END PUBLIC KEY-----'''
    rsakey = RSA.importKey(pub_key) 
    signer = PKCS1_v1_5.new(rsakey) 
    digest = SHA256.new() 
    # Assumes the data is base64 encoded to begin with
    digest.update(b64decode(data)) 
    if signer.verify(digest, b64decode(signature)):
        return True
    return False

for x in range(len(data)):
    if not verify_sign("",data[x]['signature'],data[x]['data']):
        print data[x]['data'].decode('base64')

```
Run it, and we get the flag!


Flag
------

`sometimes_needles_in_a_haystack_can_prick_you`