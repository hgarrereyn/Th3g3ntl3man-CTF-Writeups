import md5 #Must be run in python 2.7.x

#code used to calculate successive hashes in a hashchain.
ID = 3603
seed = md5.new(str(ID)).hexdigest()
goal = "1cbd7cc894b89dbeb1b000f129467887"\

prev = ""
hashc = seed
for _ in xrange(10000):
    prev = hashc
    hashc = md5.new(hashc).hexdigest()
    if(hashc == goal):
        print(prev)
        break
#print hashc
