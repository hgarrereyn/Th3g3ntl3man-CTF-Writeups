
Zeroes and Ones - 30 points
===

Writeup by poortho
------
Problem Statement:
Bit String Flicking

How many solutions are there for X in the expression:

LCIRC -3 (01011 AND X OR 10100) = 01101

Hint:

Try simplifying it?

------

Writeup
------
This problem is a simple bit string flicking equation. Let's begin.

First, LCIRC-3 means that you cycle the bits left 3 times. The inverse of LCIRC-3 is RCIRC-3, so we can rewrite the equation as `01011 AND X OR 10100 = 10101`

Then, order of operations dictates that we perform the AND then the OR.

Thus, because the OR is applied last, we know that the 2nd and 4th bit of `01011 AND X` has to be 0, the 5th bit has to be 1, and the 1st and 3rd bit can be anything.

So now we have `01011 AND X = ?0?01`. Again, we see that the 1st and 3rd bit of X can be anything. We also see that the 5th bit has to be 1, and the 2nd and 4th bit must be 0.

Thus, our answer is 2^(number of ?'s) = 2^2 = 4, which is our flag.

Flag
------

`4`
