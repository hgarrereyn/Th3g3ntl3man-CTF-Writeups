
Substitute Teacher - 25 points
===

Writeup by poortho
------
Problem Statement:
Mr. Michael S. “Mike” Rogers is the substitute teacher for the day, but he is having trouble deciphering the secret message that was left for him by the teacher. Mr. Rogers knows the note is in English, but that’s about all. Can you help him? [ENCRYPTED.txt](ENCRYPTED.txt)

Hint:

Frequency analysis.

------

Writeup
------
Based on the statement and the title, it's pretty obvious that this is a simple substitution cipher. We can use [quipqiup](quipqiup.com) to solve this.

Plugging it in, we get:

```
	In cryptography, a substitution cipher is a method o? encoding by which units o? plainte?t are replaced with cipherte?t, according to a ?i?ed system; the "units" may be single letters (the most common), pairs o? letters, triplets o? letters, mi?tures o? the above, and so ?orth. The receiver deciphers the te?t by per?orming the inverse substitution. (Wikipedia.org, "Substitution cypher") This is, ?or your sake, a completely normal English te?t. We were so nice, we decided to leave capitalization in the encrypted te?t... & punctuation! Aren't we nice. There is a relatively normal letter distribution in this te?t, so it shouldn't have been too di??icult to solve. Anyway, congratulations! Here is your ?lag: only_slightly_better_than_caesar
```

While there are some question marks, we still obtain the full flag.

Flag
------

`only_slightly_better_than_caesar`