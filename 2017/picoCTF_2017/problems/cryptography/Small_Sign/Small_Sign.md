# Small Sign

#### Writeup by Valar_Dragon

* **Cryptography, RSA Key Forgery**
* *140 points*
* This service outputs a flag if you can forge an RSA signature!
nc shell2017.picoctf.com 27465
[smallsign.py](smallsign.py)

If we connect to the server, we see that it gives us a RSA modulus, public exponent, and a maximum of 1 minute for it to encrypt and return any message we'd like. Once we've encrypted as many messages we'd like in our 1 minute time frame, it asks us to forge an RSA signature of a number they give.

The equations for encrypting and decrypting RSA Signatures are (assuming no padding, as is the case in this problem):

$$ c \equiv m^d \bmod N$$
$$ m \equiv c^e \bmod N$$
The modulii are generated securely, so theres no way we can factor those in a reasonable amount of time. But notice:
$$ c_1c_2  \bmod N \equiv m_1^dm_2^d \bmod N\equiv (m_1m_2)^d \bmod N$$

If we multiply two ciphertexts, the result of decrypting the ciphertexts will be the product of the original two messages!

So this makes our plan for forging pretty clear, we need to get the factors for our challenge encrypted in the first phase
and then multiply the ciphertexts of those factors together. Except we don't know our challenge beforehand. The smaller the prime p, the more multiples of it will exist on range $[0,2^{32})$, so to increase our chances of being able to factor our random number we should get the ciphertexts of the smallest primes in the first phase. In mathematics terminology, we are looking for a challenge that is B-smooth, where B is the index of the largest prime we are looking at.

So we just have to keep on trying to get the server to sign primes with the varying modulii, until we get a challenge that is B-smooth.

@ifm-tech wrote an awesome socket connector for this problem, so handling talking to the server became easy.

Getting the server to sign our messages takes awhile, so since we can't sign that many messages in one minute, and so it will take awhile before we get a challenge which we can fully factor into our small signed primes. So we start our [solution](solution.py), and go take a snack break, and then get the output:

```
$ python solution.py
We are looking at the first 168 primes
The largest prime we are obtaining is: 997
N: 23225724441260502163156858665541141018496104030765636336117495388452692752434551594356844301202757041498963343119776192971642650182341076075417853017963895654682907267507286893804382438104343728892184884725615652446029484470272738148082755208363740506711977494914732601051143901275174287629202627440351925877668239347476737619227138812585842151289661062861262965797206728938828440224425220049757239538828196446047245802293245569271831668627522474196683044076122265421666860419599298098813130818090983589816598084188896610492178986114840909079430074106751125367318111724015857433263606125379722651479325752520259889833

e: 65537

Done signing
Challenge: 1376397218

[2, 7]
Not fully factored
... <SNIP> ...
Not fully factored
Trying another iteration
N: 22222223266063880824151738523108932773683502205946922126395985656042776887111566249662284686720535925154927145294383689670743324701285415708765126660160055206471344943617192489145489058445612712791386819918849645320061889512498863436947807759584343055514570295431751957461574692165057498840925358522939303618079808372737081334870743398907529317254507082344471767854174786478680032084547254009589257992485301545754407174597193764569996342462430344753770379551006822573210288749698655245063732686224347409945959099675047318092421510183766462303784003917855223201640318019546979850657160430769416204335568349320120627599

e: 65537

Done signing
Challenge: 517194738

[2, 3, 3, 157, 197, 929]
21196551478776366791946737143923132659627817410974557628711611202905767761222602300771768239576768236096266199934553163731151613705788012484098376330512817793232983875474491249946099361975940350011595999665752717661821377952737646065850798545894003963763678218517505918274271494554382693969261463088137761054768782633205399308542037408962089614715933869756383713279518389690436376178337630369159979006126319842797929849044074933572007017462374901894191798123231314185483380674863854114106470057173760010686740585807219735365699737276761743417716992691495174132330056012134405925192803173793281342390647293692945490362
517194738
> Congrats! Here is the flag:
>  c1eed6a065f7b67a392a5ab8c1a9e9e2


>
Solution obtained in 10 tries!
0.661229 seconds process time
It took 263.702187061 seconds of actual time
```

So this took a reasonable amount of time to complete!
