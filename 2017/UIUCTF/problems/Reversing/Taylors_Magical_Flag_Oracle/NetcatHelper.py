import socket
import re
import time
import string

class NetcatHelper:
	def __init__(self, host, port):
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket.connect((host, port))
		sig = self._socket.recv(4096)

	def sign(self, val):
		start = time.time()
		self._socket.sendall(bytes(val + '\n','UTF-8'))
		sig = self._socket.recv(4096)
		roundtrip = time.time() - start

		return roundtrip , sig



def main():
	sigs = {}
	nc = NetcatHelper('challenge.uiuc.tf', 11340)
	base = "flag{"
	printables = string.printable[:-5]
	while(True):
		print("starting new loop")
		print(base)
		nc.sign(base+'#f')
		curtime1, sig = nc.sign(base+'ff')
		curtime1 = x_round(curtime1)
		print(curtime1)
		curtime2, sig = nc.sign(base+'gg')
		curtime2 = x_round(curtime2)
		print(curtime2)
		curtime = min(curtime1,curtime2)

		for i in printables:
			newtime,sig = nc.sign(base+i+'zz')
			if(sig[:2]!=b'No'):
				print(sig)
			if(x_round(newtime) > curtime):
				print(curtime)
				print(newtime)
				newtime,sig = nc.sign(base+i+'zz')
				if(x_round(newtime) > curtime):
					print(curtime)
					print(newtime)
					base += i
					print(base)
					break

	return True

def x_round(x):
    return(round(x*4)/4)

main()
