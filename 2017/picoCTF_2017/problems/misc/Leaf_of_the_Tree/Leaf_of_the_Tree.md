# Leaf of the Tree

* **Misc**
* *20 points*
* Description: We found this annoyingly named directory tree starting at /problems/a45d1519bd193bc3a273744c83fad1e2. It would be pretty lame to type out all of those directory names but maybe there is something in there worth finding? And maybe we dont need to type out all those names...? Follow the trunk, using cat and ls!

So this is a pretty easy challenge! We know from the harder version of this challenge "Leaf of the Forest", that the file is named flag. The command find shows all the files and subdirectories, tree style. So if we just do `file | grep flag`, it'll give us the path to the flag!

```
valar@valardev-Vostro-3460-mint ~/Code/CTF/ezCTF/simple rop $ ssh valar_dragon@shell2017.picoctf.com
Congratulations on setting up SSH key authentication!
Here is your flag: who_needs_pwords_anyways
valar_dragon@shell-web:~$ cd /problems/a45d1519bd193bc3a273744c83fad1e2
valar_dragon@shell-web:/problems/a45d1519bd193bc3a273744c83fad1e2$ find | grep flag
./trunk/trunk9ef5/trunkded5/trunk3f6a/trunk6034/trunk41fe/trunkb847/trunk7d34/flag
valar_dragon@shell-web:/problems/a45d1519bd193bc3a273744c83fad1e2$ cat trunk/trunk9ef5/trunkded5/trunk3f6a/trunk6034/trunk41fe/trunkb847/trunk7d34/flag
1510e551a2821bd027da10a7653814c8
```

Our flag: `1510e551a2821bd027da10a7653814c8`!
