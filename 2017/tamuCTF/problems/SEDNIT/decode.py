def main():
    modulus = int("A9625641EE2E381A4A887EA3A8AE900DD1E27FD9184F2E01EA486A234909A22475F34B034B48E9B6FB407895B9EA66694A4951B032FBE60F11DFB1D145BB765F66B72FC7E0E1F938455620F141A5A85B2EF049F55C5B33E351943506889F826D6936DEC658B8926A26273C7B8E8AC9AF7123D106515F76ED37FC7C513AC19DA9",16)
    e = 65537
    p = int("00:b6:a0:fc:62:b3:d4:cd:68:06:cb:54:e5:0e:65:08:4a:49:b3:49:12:40:95:cb:9c:2c:de:40:f9:31:b5:6c:d9:1d:a6:80:e4:0c:ca:75:a0:0b:2c:4a:38:8b:5d:d9:15:87:71:6e:fd:c7:cf:5a:5b:90:88:37:83:b4:f3:fd:3d".replace(":",""),16)
    assert modulus % p == 0
    q = modulus //p
    d = modinv(e,(p-1)*(q-1))
    a = ""
    c = b"HPDng5QcgvfhFuVLfMrs1+kg3cyo2GEGwxdTICOsAYgpTA2qNuTBHetrfmVMDr1n2Iu1D7lTqSGY/eH/ZGbryyBr3MuOoc+R7m2ipxl1cL/5e/UaPP0rplohjCxduEDil7WlrLfwFR8GCGhF1usgV9gzo3Ok12v8J4veejWPe4k="
    import base64
    hexString = base64.b16encode(base64.standard_b64decode(c))
    print(hexString)
    c = int(hexString,16)
    msg = pow(c,d,modulus)
    print(msg)
    import binascii
    print(binascii.unhexlify(hex(msg)[2:]))
def extended_gcd(aa, bb):
    """Extended Euclidean Algorithm,
    from https://rosettacode.org/wiki/Modular_inverse#Python
    """
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
    """Modular Multiplicative Inverse,
    from https://rosettacode.org/wiki/Modular_inverse#Python
    """
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m

main()
