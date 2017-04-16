# Much Ado About Hacking
#### Writeup by hgarrereyn
* **Reverse Engineering**
* *165 points*
* Description: In a lonely file, you find prose written in an interesting style. What is this Shakespearean play? What does it have to say? How could one get it to produce this ending?

# Solution

From the title and the file extension `.spl`, we are able to figure out that the provided file is written in the [Shakespeare Programming Language](https://en.wikipedia.org/wiki/Shakespeare_Programming_Language), an esoteric programming language.

Our goal is to find the input to the program that outputs the provided [ending]():

[**ending.txt**]()
```
tu1|\h+&g\OP7@% :BH7M6m3g=
```

I had encountered this language before, but found it quite helpful to refer to the [documentation](http://shakespearelang.sourceforge.net/report/shakespeare/) while stepping though the program.

My plan to solve this challenge was twofold:
1. compile an executable to test my inputs
2. translate the program to python and reverse engineer it

# Step 1 - compile the executable

I used `spl2c` to transpile the `spl` file to a `c` program. Then I used `gcc` to compile.

*It took quite a bit of fiddling to get the right compile flags and SPL version. I won't go into detail on exactly how I compiled because it's not exactly relevant to the problem.*

*However, [this](https://stackoverflow.com/questions/1948372/compiling-and-executing-the-shakespeare-programming-language-translator-spl2c-on) StackOverflow post was added as a hint and helped me figure out how to compile.*

At this point I had a binary that could be run like so:

```
$ ./muchado
```

It seemed to wait for user input so I tried typing a few things in and hitting enter but the program didn't seem to print anything out.

Let's reverse engineer the code and see if we can figure out what's going on.

# Step 2 - reverse engineering

To start, I simply went line by line and rewrote equivalent pseudo-python code. *Note: The python code doesn't actually work, it just served as a useful reference*

### Initialization

Let's begin!

The first few lines simply define variables. For simplicity, we will use the same variable names in python:

```spl
Much Ado About Hacking.

Benedick, a budding young hacker.
Beatrice, a veteran exploiter.
Don Pedro, a good friend of the others.
Don John, he is just kinda there.
Achilles,  I thought he was from Greece.
Cleopatra, now this is just getting ridiculous.
```

```python
### Define variables (all integers):
# benedick
# beatrice
# don_pedro
# don_john
# achilles
# cleopatra
```


### Scene I

Now the program begins. In SPL, scenes act as subroutines that can be branched to.

Initially, no characters are on the stage. When a character enters the stage, *deonoted by Enter and Exit*, it can interact with other characters.

Commands are issued by writing the character's name followed by the command. The command is applied to the *other* character on the stage.

So for example, in the first few lines, we have:

```spl
Scene I: Benedick learns his place.

[Enter Beatrice and Don John]

Beatrice:
You are nothing!

[Exit Don John]
```

When Beatrice says "You are nothing!", it sets the value of Don John to zero (because he is the other actor on the stage). It is equivalent to:

```python
don_john = 0
```

Then we see the same for Don Pedro:

```spl
[Enter Don Pedro]

Beatrice:
You are nothing!

[Exit Don Pedro]
```
```python
don_pedro = 0
```

Now in order to set a non-zero value, you have to use adjectives plus a noun. Each noun is either `1` or `-1` based on whether it is a positive or negative noun and each additional adjective multiplies that value by `2`.

In the lines:

```spl
[Enter Achilles]

Beatrice:
You are as proud as a bold brave gentle noble amazing hero.

[Exit Achilles]
```

Achilles is set to the value of the string `bold brave gentle noble amazing hero`.

*Note: when a character says "You are as * as ..." it means the same as "You are equal to ..."*

`Hero` is a positive noun, so it has the value `1`. Then there are 5 adjectives that each multiply by `2`. So our final value is: `2^5 = 32`.

Therefore, equivalent python is:

```python
achilles = 32
```

In the next lines, Cleopatra is set:

```spl
[Enter Cleopatra]

Beatrice:
You are as vile as the difference between a beautiful gentle bold fair peaceful sunny lovely flower and Achilles.

[Exit Cleopatra]
```

In this case, a subtraction operation is performed. Cleopatra is set to the value of `beautiful gentle bold fair peaceful sunny lovely flower` minus the value of `Achilles`. *In this case, Achilles corresponds to a variable and not the value `1`*.

`beautiful gentle bold fair peaceful sunny lovely flower` = `2^7` = `128`

So Cleopatra is set to `128 - 32` = `96`

```python
cleopatra = 96
```

Our first scene looks like this:

```python
# Scene I:
	don_john = 0
	don_pedro = 0
	achilles = 32
	cleopatra = 96
	benedick = 0
```

### Scene 2

Benedick and Beatrice are still on stage from the last scene. Let's examine the first command:

```spl
Beatrice:
Open your mind! Remember yourself.
```

Here she issues two commands:

* `Open your mind!` - reads a character from input and sets Benedick to it's integer value
* `Remember yourself.` - pushes the value of Benedick onto his stack

Now, I omitted this before, but all characters have an integer stack that they can push and pop values from. So, in our initialization, let's create an array that represents Benedick's stack:

```python
benedick_stack = []
```

So these lines translate to:

```python
benedick = readchar()
benedick_stack.append(benedick)
```

The next lines are:

```spl
Benedick:
You are as red as the sum of yourself and a tree.
Am I as lovely as a cunning charming honest peaceful bold pony?

Beatrice:
If not, let us return to scene II.
```

Which translate to:

```python
beatrice += 1

if not benedick == 32:
	goto: S2
```

The next lines are:

```spl
Benedick:
You are as worried as the sum of yourself and a Microsoft.

Beatrice:
Recall your father's disappointment!
```
*Note: Microsoft is a negative noun ;p*
```python
beatrice -= 1
benedick = benedick_stack.pop()
```

### Scene 3
