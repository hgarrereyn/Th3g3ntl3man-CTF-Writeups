# Coffee
#### Writeup by hgarrereyn
* **Reverse Engineering**
* *115 points*
* Description: You found a suspicious USB drive in a jar of pickles. It contains this [file]().

# Solution

The file we are given is a `.class` file which is what you get when you compile a `.java` file.

What happens when we run this file?

```
$ java freeThePickles
Error: Could not find or load main class freeThePickles
```

Hmm, it couldn't find a class named `freeThePickles`, perhaps someone changed the filename after compiling it.

Let's try to decompile this file and see what we get.

I found that the [JAD Decompiler](http://www.javadecompilers.com/jad) was well suited for this task.

### Using JAD to decompile

Once you add the `jad` binary to your path, you can run:

```
$ jad freeThePickles.class
Parsing freeThePickles.class... Generating problem.jad
```

You obtain a `.jad` source file:

```java
// Decompiled by Jad v1.5.8g. Copyright 2001 Pavel Kouznetsov.
// Jad home page: http://www.kpdus.com/jad.html
// Decompiler options: packimports(3)
// Source File Name:   problem.java

import java.io.PrintStream;
import java.util.Arrays;
import java.util.Base64;

public class problem
{

    public problem()
    {
    }

    public static String get_flag()
    {
        String s = "Hint: Don't worry about the schematics";
        String s1 = "eux_Z]\\ayiqlog`s^hvnmwr[cpftbkjd";
        String s2 = "Zf91XhR7fa=ZVH2H=QlbvdHJx5omN2xc";
        byte abyte0[] = s1.getBytes();
        byte abyte1[] = s2.getBytes();
        byte abyte2[] = new byte[abyte1.length];
        for(int i = 0; i < abyte1.length; i++)
            abyte2[i] = abyte1[abyte0[i] - 90];

        System.out.println(Arrays.toString(Base64.getDecoder().decode(abyte2)));
        return new String(Base64.getDecoder().decode(abyte2));
    }

    public static void main(String args[])
    {
        System.out.println("Nothing to see here");
    }
}
```

Alright, now it's obvious. The class is actually named `problem`. It is pretty obvious what will happen when we run the program but let's verify:

```
$ cp freeThePickles.class problem.class
$ java problem
Nothing to see here
```

In the source, we see a deadcode function called `get_flag` that will (hopefully) return the flag.

We have two options:
1. Reverse engineer the function
2. Modify the source code to call the function (and recompile)

### Option 1 - Reverse Engineer the function

We have two strings `s1` and `s2` with seemingly random characters. The function loops through `s1` and uses each byte value to point to the char in `s2` which is appended to a new array.

Then the array is converted to a string and decoded as base64 data.

It is quite trivial to implement this in python:

```python
import base64

s1 = "eux_Z]\\ayiqlog`s^hvnmwr[cpftbkjd"
s2 = "Zf91XhR7fa=ZVH2H=QlbvdHJx5omN2xc"

sEnc = "".join([s2[ord(x) - 90] for x in s1])

sDec = base64.b64decode(sEnc)

print(sDec)
```

This program prints out:

```
flag_{pretty_cool_huh}
```

We submit this as the flag.

### Option 2 - Modify the original program

In this case, the hidden function was trivial to implement. However, if it had been obfusicated or more complex, this solution may have been more applicable.

All we need to do is change this line:

```java
System.out.println("Nothing to see here");
```

to this:

```java
System.out.println(get_flag());
```

Then we can recompile and run. (change the source extenstion from `.jad` to `.java` if necessary)

```
$ javac problem.java
$ java problem
[102, 108, 97, 103, 95, 123, 112, 114, 101, 116, 116, 121, 95, 99, 111, 111, 108, 95, 104, 117, 104, 125]
flag_{pretty_cool_huh}
```

Flag: `flag_{pretty_cool_huh}`
