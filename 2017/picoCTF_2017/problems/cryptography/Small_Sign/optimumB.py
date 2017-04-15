import numpy as np
def primesfrom2to(n):
    # http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    import numpy as np
    sieve = np.ones(n/3 + (n%6==2), dtype=np.bool)
    sieve[0] = False
    for i in range(int(int(n**0.5)/3+1)):
        if sieve[i]:
            k=3*i+1|1
            sieve[      ((k*k)/3)      ::2*k] = False
            sieve[(k*k+4*k-2*k*(i&1))/3::2*k] = False
    return np.r_[2,3,((3*np.nonzero(sieve)[0]+1)|1)]

def main():
    maximumBruteNumber = 3000
    N = 2**32
    logN = np.log(N)
    curmaximum = 0
    curindex = 0
    primes = primesfrom2to(maximumBruteNumber)
    curPi = 1
    for i in range(0,len(primes)):
        curPi = curPi / (i+1)
        curPi *= logN
        curPi = curPi / np.log(primes[i])
        if(curPi / (i+16) > curmaximum):
            curmaximum = curPi / (i+16)
            curindex = i
    print(primes[curindex])
main()
