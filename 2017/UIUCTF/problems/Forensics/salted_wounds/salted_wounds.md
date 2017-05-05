## salted wounds

#### Writeup by poortho
* **Forensics**
* *200 points*
* There are some challenges I'd rather forget.
* Files:
  * [zmap.pdf](https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/blob/53ee63b2d47c9497d05fdc8b0109c76d9c01241e/2017/UIUCTF/problems/Forensics/salted_wounds/zmap.pdf)
* 11 Solves

# Solution

Opening the PDF, there doesn't seem to be anything immediately useful.

Running pdf-parser on the pdf gives us this:
```
$ pdf-parser --stats zmap.pdf
Comment: 3
XREF: 0
Trailer: 0
StartXref: 1
Indirect object: 322
  258: 1, 2, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 56, 57, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 84, 85, 87, 117, 118, 122, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 149, 150, 155, 156, 164, 165, 166, 188, 189, 190, 191, 192, 193, 194, 197, 200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228, 230, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 266, 267, 268, 269, 277, 278, 279, 280, 285, 286, 287, 289, 290, 291, 292, 297, 298, 299, 301, 302, 303, 304, 309, 310, 311, 313, 314, 315, 325, 326, 339, 340, 341, 342, 343, 346, 357, 358, 359, 360, 361, 362, 381, 382, 384, 385, 386, 391, 392, 393, 395, 396, 397, 398, 399, 400, 401, 416, 417, 418, 419, 420, 425, 426, 427, 429, 430, 431, 432, 433, 434, 447, 448, 449, 451, 452, 453, 454, 455, 460, 461, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 494, 495, 497, 498, 499, 508, 509, 510, 511, 515, 516, 517, 534, 535, 561, 563, 565, 567, 569, 571, 573, 575, 577, 581, 582, 583, 584, 585, 586, 595, 596, 597
 /Catalog 1: 603
 /ObjStm 2: 611, 612
 /Page 15: 101, 148, 163, 265, 276, 324, 338, 356, 380, 415, 446, 459, 493, 507, 533
 /XObject 44: 144, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 199, 201, 203, 205, 207, 209, 211, 213, 215, 217, 219, 221, 223, 225, 227, 229, 231, 270, 271, 272, 328, 329, 363, 405, 441, 450
 /XRef 1: 613
 /ZmbeddedZile 1: 605
```

There's an embedded file in the PDF! We can extract this using pdf-parser.
```
$ pdf-parser --object 605 --raw --filter zmap.pdf > out
```

Looking at `out`, it's base64. We can decode this like so (you'll have to remove the beginning part before you do this):
```
$ base64 -d < out > pic1
$ file pic1
out1: PNG image data, 1221 x 651, 8-bit/color RGBA, non-interlaced
```

It's a PNG file! Unfortunately, running things such as strings and stegsolve don't work.

After a bit of guessing, we find out that the image contains LSB steganography.

Here's my script:
```python
from PIL import Image
def rgb2hex(r, g, b):
    return '{:02x}{:02x}{:02x}'.format(r, g, b)
im = Image.open("pic1.png") #whatever you named the PNG file
pix = im.load()
s = ""
f = ""
print pix[0,0]
print pix[0,1]
print pix[0,2]
for x in range(72):
    for y in range(3):
        if pix[0,x][y] % 2 == 0:
            s += '0'
        else:
            s += '1'
        if len(s) == 8:
            f += chr(int(s,2))
            s = ""
print f
```

Run it, and we get the flag!
# Flag

`flag{say_y0ull_r3memb3r_m3}`
