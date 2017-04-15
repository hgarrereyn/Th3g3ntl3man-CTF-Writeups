import socket
import re

# Harrison Green ( @ifm-tech ) made an awesome Netcat helper for this challenge!
class NetcatHelper:
	def __init__(self, host, port):
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket.connect((host, port))

		# Just predicting the packets
		ignore = self._socket.recv(4096)
		dataInitial = self._socket.recv(4096).replace('\n',' ')

		# parse
		self.N = int(re.search(r'N: ([0-9]*)', dataInitial).group(1))
		self.e = int(re.search(r'e: ([0-9]*)', dataInitial).group(1))

	def getInitial(self):
		return self.N, self.e

	def sign(self, num):
		self._socket.sendall(str(num) + '\n')

		ignore = self._socket.recv(4096)
		sig = int(re.search(r'.([0-9]*)', self._socket.recv(4096)).group(0))
		#print(sig)
		return sig

	def getChallenge(self):
		self._socket.sendall('-1\n')

		ignore = self._socket.recv(4096)
		chal = int(re.search(r'.([0-9]*)', self._socket.recv(4096)).group(0))

		return chal

	def solve(self, solution):
		self._socket.sendall(str(solution) + '\n')

		while True:
			data = self._socket.recv(4096)

			print('> ' + data)

			if not data:
				break


## Do crypto magic down here
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
    sigs = {}
    nc = NetcatHelper('shell2017.picoctf.com', 27465)

    N, e = nc.getInitial()

    print('N: ' + str(N) + '\n')
    print('e: ' + str(e) + '\n')

    for i in primes:
    	sigs[i] = nc.sign(i)

    	#print(str(i) + ' : ' + str(sig) + '\n')
    print("Done signing")
    c = nc.getChallenge()
    solution = 1
    print('Challenge: ' + str(c) + '\n')
    factors = []
    for i in primes:
        while(c % i == 0):
            factors.append(i)
            c = c//i
            solution = (solution*sigs[i]) % N
    print(factors)
    if(c != 1):
        print("Not fully factored")
        return False
    print("Forgery is: " + str(solution))
    print("Which decodes to: " + str(pow(solution,e,N)))

    nc.solve(solution)
    return True

primes = primesfrom2to(1000)
print("We are looking at the first %s primes" % len(primes))
print("The largest prime we are obtaining is: %s" % primes[-1])

import time
t0 = time.clock()
t01 = time.time()
iterationnum = 1
while(main()!=True):
	print("Trying another iteration")
	iterationnum +=1
print("Solution obtained in %s tries!" % iterationnum)
print(str(time.clock() - t0) +" seconds process time")
print("It took " + str(time.time() - t01) +" seconds of actual time")
