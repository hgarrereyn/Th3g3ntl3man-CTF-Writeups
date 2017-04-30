import binascii
import rsa
import sys

key = rsa.PublicKey.load_pkcs1(b'XXXXXXXX')
message = "right below".encode("ASCII")
print(message)
print(binascii.hexlify(message))
yn = input("have you read the terms and conditions? [y/N] ")

if yn.lower() in ['y', 'yes']:
    sighex = input("OK, sign right below ")
    try:
        sig = binascii.unhexlify(sighex)
    except:
        print("signatures must be valid hex")
        sys.exit(0)
    print("verifying rsa signature {} for message \"right below\"...".format(sighex))
    try:
        rsa.verify(message, sig, key)
        print("thanks!")
        with open("flag.txt", "r") as flag:
            print(flag.read())
    except:
        print("that doesn't look like a valid signature")
else:
    print("""
TERMS AND CONDITIONS
* you get to play our ctf
* we get your firstborn child
* you must wear only natural fibers while playing our ctf
* we must use the latest versions of all libraries
* you must burn no more than 7 and no less than 3 paddington bear books prior to attempting the ctf
* we must only use ASCII encodings
* you must crucify a small woodland animal every time you submit a flag
* we must use 2048-bit keys with e = 3
DATED: 2015-07-29""")
