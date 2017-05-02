
Remember md5? - 40 points
===

Writeup by poortho
------
Problem Statement:
Remember md5?

Oh. Those good old days of md5 and huge rainbow tables. I get nostalgic just thinking about it. Well, you can’t use one of those to break my password. It still isn’t very secure though. I only used my favorite characters ‘a’, ‘b’, and ‘c’. I remember it being about 14 characters long. The hash is 1b657b7fe26eda5b3c1309d340f1674d.

Hint:

When all else fails, try brute force.

------

Writeup
------
To solve this problem, we can simply brute force all possible combinations of the characters a, b, and c.

Note that the problem said 'about 14 characters' - this means that it may not be exactly 14. Here's my code:
```python
import itertools
import md5

for x in range(20):
    keywords = [''.join(i) for i in itertools.product(['a','b','c'], repeat = x)]
    for y in keywords:
        if md5.new(y).hexdigest() == "1b657b7fe26eda5b3c1309d340f1674d":
            print y
```

Run it, and we get the flag!

Flag
------

`abbabcbabcbabcb`
