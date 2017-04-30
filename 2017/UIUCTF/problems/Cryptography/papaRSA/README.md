# PapaRSA - 250 points

#### Writeup by Valar_Dragon
* **Cryptography**
* 6 Solves (We were first solve!)

## Problem

I screwed up with babyrsa and made it too easy! I fixed it and now it's paparsa!
[paparsa.py](paparsa.py) [paparsa.txt](out.txt)

## Solution

We're given the output of

```python
from Crypto.PublicKey import RSA

key = RSA.generate(4096, e=5)
msg = "this challenge was supposed to be babyrsa but i screwed up and now i have to redo the challenge.\nhopefully this challenge proves to be more worthy of 250 points compared to the 200 points i gave out for babyrsa :D :D :D\nyour super secret flag is: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\nyou know what i'm going to add an extra line here just to make your life miserable so deal with it"
m = int(msg.encode("hex"), 16)
c = pow(m, key.e, key.n)

f = open("paparsa.txt", "w")
print >> f, "n = {}".format(key.n)
print >> f, "e = {}".format(key.e)
print >> f, "c = {}".format(c)
```

Looks like we're not getting as lucky as last problem, we have a pretty long message this time. `len(msg) = 406`, so

$$ m^e ~= 2^{(406*8)^5} = 2^{16240} $$
which is waay bigger than our modulus.

We can however use Coppersmith's method, which uses the Lenstra–Lenstra–Lovász lattice basis reduction algorithm (LLL), to solve this!

We can however use Coppersmith's method. What it does is: for a monic polynomial modulo N, it finds the zeroes for the polynomial where x < N^(1/degree(f(x)) - epsilon), where epsilon essentially determines the running time. (epsilon is normally around 1/7th or 1/8th) Re-arranging that, and ignoring epsilon, as long as our x follows: x^degree(f(x)) < N, coppersmith can solve it! It runs rather quickly, and thankfully sage already has it implemented! (It is the small_roots function)

We can treat Coppersmith's method as a blackbox, but the key behind how it works is it finds smaller polynomials that share the same small zero of the original polynomial, and it solves those smaller polynomials.

So in our case, we can make the polynomial:
$$ f(x) = (message + x)^e - C \mod N$$

Notice that when message + x is equal to the plaintext, f(x) = 0! If we have x, then we have the plaintext!
Message in our case will be the string they gave us, but with those X's replaced with null bytes, since we can't have x being negative.
However, null bytes wouldn't render here, so I'll keep them as X's in strings. Just remember we are really working with them being null bytes.

Buuuut there's one issue. The portion that's the difference, `XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\nyou know what i'm going to add an extra line here just to make your life miserable so deal with it` is 159 characters long.

This makes the maximum value for x:
$$x < (2^8)^{159} = 2^{1272}$$
$$x^e < 2^{6360}$$
which is way bigger than N, so we can't use Coppersmith.

Or can we!

We know the difference between what we are given, and what the actual encrypted message is, starts at the 60th character from the left, or the 100th counter counting from the right.
The difference in those last 99 characters is all 0, since they will be the same as whatever they are in `message`.
If a number ends in a null byte, that means it is divisible by 256.
Thus that means whatever the difference `x` is, it must be a multiple of $$ 256^99 = 2^792 $$.

So that means the polynomial f(x) will have the exact same zeroes as polynomial:

$$ g(x) = (message + 2^{792}x)^e - C$$

But now we have lowered the maximum value for x!
Originally $$x < 2^{1272}$$, but now we've changed that to

$$x*(2^{792}) < 2^{1272}, x < 2^{480}$$
$$x^e < 2^{2040} < N$$
So we can use coppersmith to solve this! For Coppersmith we have to make the polynomial monic, since g(x) is no longer monic, but sage can do this for us.
But if we put our monic version of the polynomial into sage, we get no results.
Thats odd.

Sage's default value for epsilon is 1/8, so lets see what upperbound that would give.
$$\frac{1}{5} - \frac{1}{8} = \frac{3}{40}$$
$$2^{{4096}^\frac{3}{40}} = 2^{\frac{4096*3}{40}} = 2^{307.2} < x$$

No wonder it didn't work by default!
Well no problem, if we just adjust epsilon we'll get our solution!

```python
sage: msg = "this challenge was supposed to be babyrsa but i screwed up and now i have to redo the challenge.\nhopefully this challenge proves to be more worthy of 250 points compared to the 200 points i gave out for babyrsa :D :D :D\nyour super secret flag is: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\nyou know what i'm going to add an extra line here just to make your life miserable so deal with it"
sage: msg = msg.replace('X','\x00')
sage: import binascii
sage: message = int(binascii.hexlify(msg),16)
sage: e = 5
sage: c = 321344338551168130701947757669249162791535374419225256466002854387287697945811581844875867845545337575193797350159207497966826027124926618458827324785590115214765980153475875175895244152171945352397663605222668892070894285036685408001675776259216704639659684767335997326195127379070104670798191048101430782486785148455557975065509824478935393935463232461294974471055239751453456270779997852527271795223623224696998441762750417393944955667837832299195592347653873362173157136283926817115042942127695355760288879165245940595259284499711202547364332122472169897570069773912201877037737474884548477516093671861643329899650704311880900221217905929830674467383904928054908475945599046498840246878554674443087280023564313470872269644230953001876937807402083390603760508851259383686896871724061532464374712413952574633098739843484563001012414107193262431117290853995664646176812763789444386869148000606985026530596652927567162641583951775993815884965569050328445927871220492529331846189285588168127051152438658813934744257031316581112434690871286836998078235766836485498780504037745116357109237384369621143931229920342036890494878183569174869563857473355851368119174926388706612127773670862261189669510108216517652686402185979222505401328291
sage: n = 805467500635696403604126524373650578882729068725582344971555936471728279008969317394226798274039587275908735628164913963756789131471531490012281262137708844664619411648776174742900969650281132608104486439462068493207388096754400356209191212924158917441463852311090597438686723680422989566039830705971272945580630621308622704812919416445637277433384864510484266136345300166188170847768250622904194100556098235897898548354386415341541887443486684297114240486341073977172459860420916964212739802004276614553755113124726331629822694410052832980560107812738167277181748569891715410067156205497753620739994002924247168259596220654379789860120944816884358006621854492232604827642867109476922149510767118658715534476782931763110787389666428593557178061972898056782926023179701767472969849999844288795597293792471883445525249025377326859655523448211020675915933552601140243332965620235850177872856558184848182439374292376522160931072677877590262080551636962148104050583711183119856867201924407132152091888936970437318064654447142605921825771487108398034919404885812834444299826080204996660391375038388918601615609593999711720104533648851576138805705999947802739408729788376315233147532770988216608571607302006681600662261521288802804512781133
sage: ZmodN = Zmod(n)
sage: c = ZmodN(c)
sage: e = ZmodN(e)
sage: message = ZmodN(message)
sage: P.<x> = PolynomialRing(ZmodN)
sage: pol = ((message + ZmodN((2**792))*x)^5) - c
sage: pol = pol.monic()
sage: pol.small_roots()
[]
sage: pol.small_roots(epsilon=1/15)
[1248984295175060908103635259382502837476510996520290172164518365629374785269360163379181788573297776902028363990820288716208404068947393627909757]
sage: xval = pol.small_roots(epsilon=1/15)[0]
sage: xval *= 2**792
sage: binascii.unhexlify(hex(Integer(message+xval)))
"this challenge was supposed to be babyrsa but i screwed up and now i have to redo the challenge.\nhopefully this challenge proves to be more worthy of 250 points compared to the 200 points i gave out for babyrsa :D :D :D\nyour super secret flag is: flag{bu7_0N_4_w3Dn3sdAy_iN_a_c4f3_i_waTcH3dD_17_6eg1n_aga1n}\nyou know what i'm going to add an extra line here just to make your life miserable so deal with it"
```

And there's our flag!
`flag{bu7_0N_4_w3Dn3sdAy_iN_a_c4f3_i_waTcH3dD_17_6eg1n_aga1n}`
This was an awesome challenge!
