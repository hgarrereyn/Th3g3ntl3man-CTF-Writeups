
Time Travel - 20 points
===

Writeup by poortho
------
Problem Statement:
Our website links to many web pages. Once upon a time, one of them displayed the flag.

Hint:

PACTF did not exist before 2015.

------

Writeup
------
Based on the problem statement, we have to look at one of the websites linked on the website. Scrolling to the bottom, we see a few links.
1. PACTF 2016
2. Statuspage
3. Phillips Academy website

We can immediately eliminate number 3 as the organizers probably do not have backend access to their school's website. We can also eliminate 2016 as it would probably get confused with last year's flags/problems.

Thus, we are left only with the statuspage. Quickly scrolling through, we don't see anything interesting. However, we can click each report for more details. Doing so for each entry gets us the flag [here](https://pactf.statuspage.io/incidents/h6c6q63bt0pl).

Flag
------

`FLAG_3NJIE9CLDIUEWD8K7T8JT2YRQP7D3762`
