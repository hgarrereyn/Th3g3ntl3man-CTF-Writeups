#!/usr/bin/python2 -u
from hashlib import sha256
from Crypto import Random
from Crypto.Random import random
from Crypto.Cipher import AES
from subprocess import check_output, STDOUT, CalledProcessError

#Get password from getPassword.py
# Now we communicate with server here to get flag

BLOCK_SIZE = 16
R = Random.new()

def pad(m):
    o = BLOCK_SIZE - len(m) % BLOCK_SIZE
    return m + o * chr(o)

def unpad(p):
    return p[0:-ord(p[-1])]

def send_encrypted(KEY, m):
    IV = R.read(BLOCK_SIZE)
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    c = aes.encrypt(pad(m))
    print (IV + c).encode('hex')

def read_encrypted(KEY,msg):
    data = msg.decode('hex')
    IV, data = data[:BLOCK_SIZE], data[BLOCK_SIZE:]
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    m = unpad(aes.decrypt(data))
    return m

def serve_commands(KEY):
    while True:
        cmd = read_encrypted(KEY)
        try:
            output = check_output(cmd, shell=True, stderr=STDOUT)
        except CalledProcessError as e:
            output = str(e) + "\n"
        send_encrypted(KEY, output)

b = 100000000

p = 174807157365465092731323561678522236549173502913317875393564963123330281052524687450754910240009920154525635325209526987433833785499384204819179549544106498491589834195860008906875039418684191252537604123129659746721614402346449135195832955793815709136053198207712511838753919608894095907732099313139446299843
g = 41899070570517490692126143234857256603477072005476801644745865627893958675820606802876173648371028044404957307185876963051595214534530501331532626624926034521316281025445575243636197258111995884364277423716373007329751928366973332463469104730271236078593527144954324116802080620822212777139186990364810367977
A = 43993758753707864275468999555616378051046246128895524402077950448045590968095556347062975883650733886606463448783537955023681654651807819553056140499549480252034709242283621414184576913569963053958329347169070766463578641163736276722204098960965479007602665014813361856996655524423702698187284010065425255093

B = pow(g,b,p)
print(B)
K = pow(A,b,p)

KEY = sha256(str(K)).digest()

print(send_encrypted(KEY,"ThisIsMySecurePasswordPleaseGiveMeAShell\n"))
cur = "potat"

# Put output in here, for encrypting, just put plain thing, for decrypting, just put a leading g
while(cur != ""):
    cur = raw_input("next line\n")
    if(cur[0:1]=="g"):
        print(read_encrypted(KEY,cur[1:]))
    else:
        print(send_encrypted(KEY,cur))
print()
# if pw == password:
#     serve_commands(KEY)
# else:
#     send_encrypted("Invalid password!\n")
