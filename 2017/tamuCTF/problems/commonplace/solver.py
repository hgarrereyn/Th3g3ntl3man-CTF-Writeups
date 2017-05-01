"""
    author: Valar_Dragon
    Most of the code is taken from https://github.com/ValarDragon/CTF-Crypto/blob/master/RSA/RSATool.py
    This file is for solving the problem "commonplace" in TAMU CTF
"""
def main():
    c1= 113813183669138175934253327749893332943694663202917548419879979936113727807991975380789093990918555434528794103836763855754041437680205960804923000204634278886935954216863968768728071369713538578259340141128572389122463301812462867702677705382960446527304300249850434659234034059007093429421932891935128492191
    c2= 59592662056482906433736561597578166591998193181333493694719960644468628650001544958506724082784316619123428485133794736006814756155380574695012682374575344544660341665720360568288716218348833128874115263588724816642658565570037107367937645463033170935908829842437861807209356311867606830691669626376334399022
    e1= 65537
    e2= 65539
    N= 140216241479851920702913185519800783649753498440837063273589417093260541429672666580261240688082289292539743280956921925064315299379164225490594370970136829532546393944568725668725847968007488489962801409779037532011361897601886281985696292232495507470403707038858415259380311715703788874074076955567300548823

    msg = commonModulusPubExpSamePlainText(e1,e2,c1,c2,N)
    print(msg)
    import binascii
    print(binascii.unhexlify(hex(msg)[2:]))

def commonModulusPubExpSamePlainText(e1,e2,c1,c2,n):
    """
        Solves for message if you have two ciphertexts of the same message
        encrypted with different public exponents and same modulus.
        Source: https://crypto.stackexchange.com/questions/16283/how-to-use-common-modulus-attack
    """
    GCD, s1, s2 = extended_gcd(e1, e2)
    assert GCD == 1
    assert s1*e1 + s2*e2 == 1
    message = 1
    if(s1 < 0):
        inv = modinv(c1,n)
        message = message*pow(inv,-1*s1,n) % n
        message = message*pow(c2,s2,n) %n
    elif(s2 < 0):
        inv = modinv(c2,n)
        message = message*pow(inv,-1*s2,n) % n
        message = message*pow(c1,s1,n) %n
    else:
        message = pow(c1,s1,n)*pow(c2,s2,n) % n
    return message

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
