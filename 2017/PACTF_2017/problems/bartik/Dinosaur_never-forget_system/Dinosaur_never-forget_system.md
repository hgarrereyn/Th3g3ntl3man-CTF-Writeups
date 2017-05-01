
Dinosaur Never-forget System - 30 points
===

Writeup by poortho
------
Problem Statement:
Those Dinosaurs…

The dinosaurs need some way to archive their messages and news for the future, so they created the Dinosaur Never-forget System. They wanted the login to be public, but they also didn’t want it to be too easy to find. So they hid it in a system more antiquated than the dinosaurs themselves.

dinosaurneverforgetsystem.tk

Hint:

They kept records, too.

------

Writeup
------
Going to the link, it doesn't look like there is anything there. However, the problem title also references DNS, or domain name service. We can lookup the DNS records of the domain using an online tool.

I used [this website](), which gives us:
```
edger entry available at LEDGER subdomain -- flag: dinosaurs_must_stay_informed
```

Flag
------

`dinosaurs_must_stay_informed`