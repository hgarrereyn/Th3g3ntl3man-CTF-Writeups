
Authorization of Time - 55 points
===

Writeup by poortho
------
Problem Statement:
[qr.png](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/raw/66038b5e3e96aff65fa07ddfe5c1fb1abfa2f61a/2017/PACTF_2017/problems/bartik/Authorization_of_time/qr.png). `1489798809000`. Get me in.

Hint:

Big ben just hit `1`.

------

Writeup
------
For this challenge, we are given a qr code and a unix epoch timestamp. Converting it to a readable format tells us that the timestamp is `Sat, 18 Mar 2017 01:00:09 GMT`.

We can decode the QR code using [this](https://zxing.org/), which gives us `otpauth://totp/PACTF%3AMiles?secret=ORUW2ZK7OBQXG43FONPWE5LUL5RXK2LMONPXG5DBPFPXI2DFL5ZWC3LF`

It looks like this is a otpauth token! Looking up the format, we find out that the secret is encoded in base32. Decoding this, we get `time_passes_but_cuils_stay_the_same`.

Presumably, we have to generate the 6 digit code for this token. Looking up otpauth code online, we can simply create a totp token with the secret and timestamp to get the flag:

```python
import sys
import time
import hmac
import base64
import struct
import hashlib
import warnings


if sys.version_info[0] == 3:
    PY2 = False
    string_type = str
else:
    PY2 = True
    string_type = unicode
    range = xrange


__author__ = 'Hsiaoming Yang <me@lepture.com>'
__homepage__ = 'https://github.com/lepture/otpauth'
__version__ = '1.0.1'


__all__ = ['OtpAuth', 'HOTP', 'TOTP', 'generate_hotp', 'generate_totp']


HOTP = 'hotp'
TOTP = 'totp'


class OtpAuth(object):
    """One Time Password Authentication.
    :param secret: A secret token for the authentication.
    """

    def __init__(self, secret):
        self.secret = secret

    def hotp(self, counter=4):
        """Generate a HOTP code.
        :param counter: HOTP is a counter based algorithm.
        """
        return generate_hotp(self.secret, counter)

    def totp(self, period=30, timestamp=None):
        """Generate a TOTP code.
        A TOTP code is an extension of HOTP algorithm.
        :param period: A period that a TOTP code is valid in seconds
        :param timestamp: Create TOTP at this given timestamp
        """
        return generate_totp(self.secret, period, timestamp)

    def valid_hotp(self, code, last=0, trials=100):
        """Valid a HOTP code.
        :param code: A number that is less than 6 characters.
        :param last: Guess HOTP code from last + 1 range.
        :param trials: Guest HOTP code end at last + trials + 1.
        """
        if not valid_code(code):
            return False

        code = bytes(int(code))
        for i in range(last + 1, last + trials + 1):
            if compare_digest(bytes(self.hotp(counter=i)), code):
                return i
        return False

    def valid_totp(self, code, period=30, timestamp=None):
        """Valid a TOTP code.
        :param code: A number that is less than 6 characters.
        :param period: A period that a TOTP code is valid in seconds
        :param timestamp: Validate TOTP at this given timestamp
        """
        if not valid_code(code):
            return False
        return compare_digest(
            bytes(self.totp(period, timestamp)),
            bytes(int(code))
        )

    @property
    def encoded_secret(self):
        secret = base64.b32encode(to_bytes(self.secret))
        # bytes to string
        secret = secret.decode('utf-8')
        # remove pad string
        return secret.strip('=')

    def to_uri(self, type, label, issuer, counter=None):
        """Generate the otpauth protocal string.
        :param type: Algorithm type, hotp or totp.
        :param label: Label of the identifier.
        :param issuer: The company, the organization or something else.
        :param counter: Counter of the HOTP algorithm.
        """
        type = type.lower()

        if type not in ('hotp', 'totp'):
            raise ValueError('type must be hotp or totp')

        if type == 'hotp' and not counter:
            raise ValueError('HOTP type authentication need counter')

        # https://code.google.com/p/google-authenticator/wiki/KeyUriFormat
        url = ('otpauth://%(type)s/%(label)s?secret=%(secret)s'
               '&issuer=%(issuer)s')
        dct = dict(
            type=type, label=label, issuer=issuer,
            secret=self.encoded_secret, counter=counter
        )
        ret = url % dct
        if type == 'hotp':
            ret = '%s&counter=%s' % (ret, counter)
        return ret

    def to_google(self, type, label, issuer, counter=None):
        """Generate the otpauth protocal string for Google Authenticator.
        .. deprecated:: 0.2.0
           Use :func:`to_uri` instead.
        """
        warnings.warn('deprecated, use to_uri instead', DeprecationWarning)
        return self.to_uri(type, label, issuer, counter)


def generate_hotp(secret, counter=4):
    """Generate a HOTP code.
    :param secret: A secret token for the authentication.
    :param counter: HOTP is a counter based algorithm.
    """
    # https://tools.ietf.org/html/rfc4226
    msg = struct.pack('>Q', counter)
    digest = hmac.new(to_bytes(secret), msg, hashlib.sha1).digest()

    ob = digest[19]
    if PY2:
        ob = ord(ob)

    pos = ob & 15
    base = struct.unpack('>I', digest[pos:pos + 4])[0] & 0x7fffffff
    token = base % 1000000
    return token


def generate_totp(secret, period=30, timestamp=None):
    """Generate a TOTP code.
    A TOTP code is an extension of HOTP algorithm.
    :param secret: A secret token for the authentication.
    :param period: A period that a TOTP code is valid in seconds
    :param timestamp: Current time stamp.
    """
    if timestamp is None:
        timestamp = time.time()
    counter = int(timestamp) // period
    return generate_hotp(secret, counter)


def to_bytes(text):
    if isinstance(text, string_type):
        # Python3 str -> bytes
        # Python2 unicode -> str
        text = text.encode('utf-8')
    return text


def valid_code(code):
    code = string_type(code)
    return code.isdigit() and len(code) <= 6


def compare_digest(a, b):
    func = getattr(hmac, 'compare_digest', None)
    if func:
        return func(a, b)

    # fallback
    if len(a) != len(b):
        return False

    rv = 0
    if PY2:
        from itertools import izip
        for x, y in izip(a, b):
            rv |= ord(x) ^ ord(y)
    else:
        for x, y in zip(a, b):
            rv |= x ^ y
    return rv == 0

a = generate_totp("time_passes_but_cuils_stay_the_same",timestamp=1489798809)
print a
```

Flag
------

`808365`
