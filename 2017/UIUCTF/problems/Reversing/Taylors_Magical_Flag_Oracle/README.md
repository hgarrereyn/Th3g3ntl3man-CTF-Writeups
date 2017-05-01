## Taylor's Magical Flag Oracle - 150 points

#### Writeup by Valar_Dragon
* **Reversing**
* 63 Solves

### Problem

We set up a service to check if you've found the correct flag for this challenge. It'd take 1.7*10^147 years to brute force, so don't bother trying it.

Note: flag follows the "flag{" format and is all lowercase

Update: Scores have been reset due to a bug that caused the flag to be printed without a legitimate solve. Scripts that solve the challenge in the intended way should still work.

nc challenge.uiuc.tf 11340
[compare_flag.py](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/blob/4cd2aa69e6b21aa17fcd8d064d9658b1d7fe2430/2017/UIUCTF/problems/Reversing/Taylors_Magical_Flag_Oracle/compare_flag.py)

### Solution

If we add a print statement to compare_flag.py, and a local flag, then run it in the interpreter, it becomes pretty clear how we attack this.

```python
>>> from time import sleep
>>> from itertools import zip_longest
>>> flag = "flag{I_Think_This_Should_Be_The_Flag}"
>>> def compare_flag(input_flag):
...     if(len(input_flag) == 0):
...         return False
...     for left, right in zip_longest(input_flag, flag):
...         if(left != right):
...             return False
...         print(left,right)
...         sleep(0.25) # prevent brute forcing
...     return True
...
>>> compare_flag("flag{Is_This_It}")
f f
l l
a a
g g
{ {
I I
False
```

You can't see it on the markdown, but there was a quarter second delay between each of those prints. So this means that we can do a time-based attack to find our flag!

If there is an extra quarter second delay, we know that we have found another character of the flag.

The code used to solve this is in [NetcatHelper.py](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/blob/4cd2aa69e6b21aa17fcd8d064d9658b1d7fe2430/2017/UIUCTF/problems/Reversing/Taylors_Magical_Flag_Oracle/NetcatHelper.py),
eventually we get that the flag is flag{trchrus}, and we can verify this over the netcat connection:

```
$ nc challenge.uiuc.tf 11340
> flag{trchrus}
Yes! flag{trchrus}
```
