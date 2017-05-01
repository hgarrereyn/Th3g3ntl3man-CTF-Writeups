
Dinosaur Never-forget System (Continued) - 40 points
===

Writeup by poortho
------
Problem Statement:
Those Dinosaurs… had money?

Turns out they also created a ledger system.

Hint:

I wonder what entry you’re looking for…

------

Writeup
------
Looking back at the information we found from the previous problem, we have:
```
edger entry available at LEDGER subdomain -- flag: dinosaurs_must_stay_informed
```

This mentions a ledger subdomain. So, we perform another lookup on `ledger.dinosaurneverforgetsystem.tk`

Doing so gets us this string: `3890a940bf54bb50d2ad334d0d0ddbda8a8737b6873277412756724292e89e31`

However, this hex string doesnt decode into printable ASCII and doesnt seem to hold significance.

If we try googling the string, however, we find it on blockchain [here](https://blockchain.info/tx/3890a940bf54bb50d2ad334d0d0ddbda8a8737b6873277412756724292e89e31?show_adv=true). At the bottom, there is the flag.

Flag
------

`those_dinosaurs_sure_are_clever`