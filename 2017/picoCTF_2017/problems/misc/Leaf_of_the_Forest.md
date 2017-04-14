# Leaf of the Forest

* **Misc**
* *30 points*
* Description: We found an even bigger directory tree hiding a flag starting at /problems/ba3662836dafb25fdcb412b505b7b677. It would be impossible to find the file named flag manually...

So this is another pretty easy challenge! We know that the file is named flag. The command find shows all the files and subdirectories, tree style. So if we just do `file | grep flag`, it'll give us the path to the flag!

```
valar@valardev-Vostro-3460-mint ~/Code/CTF/ezCTF/simple rop $ ssh valar_dragon@shell2017.picoctf.com
Congratulations on setting up SSH key authentication!
Here is your flag: who_needs_pwords_anyways
valar_dragon@shell-web:~$ cd /problems/ba3662836dafb25fdcb412b505b7b677
valar_dragon@shell-web:/problems/ba3662836dafb25fdcb412b505b7b677$ find | grep flag
./forest/tree2763a4/trunk764d/trunke6d5/trunk7905/trunk0008/trunk95d7/trunkcbe5/trunk2319/branchc790/flag
valar_dragon@shell-web:/problems/ba3662836dafb25fdcb412b505b7b677$ cat forest/tree2763a4/trunk764d/trunke6d5/trunk7905/trunk0008/trunk95d7/trunkcbe5/trunk2319/branchc790/flag
395ba83a5a494eb04f43e15020577a75
```

Our flag: `395ba83a5a494eb04f43e15020577a75`!
