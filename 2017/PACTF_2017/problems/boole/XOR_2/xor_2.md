
XOR 2 - 40 points
===

Writeup by poortho
------
Problem Statement:
Miles just sent me a really cool article to read! Unfortunately, he encrypted it before he sent it to me. Can you crack the code for me so I can read the article? [Article.txt](article.txt)

Hint:

Did you know that in typical English writing, a character is the same as the one k characters in front of it about 8% of the time, regardless of k?

------

Writeup
------
As the problem title suggests, the txt given to us is xor-encoded. However, it doesnt seem to be a single character key like last time.

The hint seems to indicate frequency analysis. However, we're all lazy and don't want to do it ourselves, and it turns out there's a handy tool called [xortool](https://github.com/hellman/xortool) that can solve this for us!

Running xortool using `$ xortool -x -c ' ' article.txt` gives us the following output:

```
The most probable key lengths:
   4:   11.0%
   6:   14.3%
   8:   9.2%
  12:   20.5%
  16:   6.5%
  18:   8.1%
  20:   5.6%
  24:   11.9%
  36:   7.7%
  48:   5.4%
Key-length can be 4*n
1 possible key(s) of length 12:
frqncyislove
Found 1 plaintexts with 95.0%+ printable characters
See files filename-key.csv, filename-char_used-perc_printable.csv
```
Based on the key found, the plaintext probably has the flag! Opening up the file and ctrl+F 'flag' and we find `The flag is primes_are_cool.`

Flag
------

`primes_are_cool`
