import binascii
import math
import random
def python_rsa_bleichenbacher(msg,hashtype,msgHashed,modulusSize):
    'https://blog.filippo.io/bleichenbacher-06-signature-forgery-in-python-rsa/'
    HASH_ASN1 = {
        'MD5': b'\x30\x20\x30\x0c\x06\x08\x2a\x86\x48\x86\xf7\x0d\x02\x05\x05\x00\x04\x10',
        'SHA-1': b'\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14',
        'SHA-256': b'\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20',
        'SHA-384': b'\x30\x41\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x02\x05\x00\x04\x30',
        'SHA-512': b'\x30\x51\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x03\x05\x00\x04\x40'
    }
    # we need to forge 00 01 XX XX XX ... XX XX 00 HASH_ASN1[hashtype] HASH
    # where the XX's make the whole thing same size as modulus

    # MAKE SUFFIX
    print(msgHashed)
    targetSuffix = '0000000000' + bin(int(binascii.hexlify(HASH_ASN1[hashtype]),16))[2:] + bin(msgHashed)[2:]
    print(targetSuffix)
    print(hex(int(targetSuffix,2)))
    # s = our forgery
    # c = s^3
    # tgt = targetSuffix
    # key here is that nth bit, counting from LSB, only affects nth bit OR later in c

    # s starts out as bytes until first 1 in tgt
    s = targetSuffix[targetSuffix.rfind('1'):]
    c = sToC(s)

    initLenS = len(s)
    for index in range(initLenS,len(targetSuffix)):
        if(c[len(c)-index-1]==targetSuffix[len(targetSuffix)-index-1]):
            s = '0' + s
        else:
            s = '1' + s
        c = sToC(s)

    # SUFFIX MADE!

    assert(c[-len(targetSuffix):]==targetSuffix)
    suffix ='00'+hex(int(s,2))[2:]
    print("suffix is %s" % hex(int(s,2)))
    print("suffix is %s" % hex(int(c,2)))
    # Generate prefix
    prefix = format(0,'08b') + format(1,'08b')
    prefix += ''.join([format(random.randint(1,256),'08b')]*((modulusSize-len(prefix))//8))
    assert len(prefix) == modulusSize
    print(hex(int(prefix,2)))
    import gmpy
    cRoot = gmpy.root(int(prefix,2),3)
    if(cRoot[1]==1):
        cRoot = int(cRoot[0].digits())
    else:
        cRoot = int(cRoot[0].digits())
    print(hex(cRoot))
    prefix = hex(cRoot)[2:]
    final = prefix[:-len(suffix)] + suffix
    print(final)
    print(int(final,16))
    print('0'+hex(int(final,16)**3)[2:])
    return 'potato'

def sToC(s):
    s = int(s,2)
    if(s==1):
        return '00001'
    return bin(s**3)[2:]
print(python_rsa_bleichenbacher("right below", 'SHA-256',int('b24fbe5fba106419e028be32dd049736d797815f6a6f5370579437784c51eb9f',16),2048))
