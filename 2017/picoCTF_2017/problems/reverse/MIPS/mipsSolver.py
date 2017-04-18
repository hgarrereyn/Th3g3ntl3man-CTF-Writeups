# By Harrison Green <hgarrereyn>

def a(b0,b1,b3):
	return (16777215 * b0) + (-12517375 * b1) + b3 - 1922105344

for i in range(0,256):
	for j in range(0,256):
		v = a(i,j,0)

		if abs(v) < 18176 + 256:
			b0 = i
			b1 = j
			b3 = -v
			b2 = (b3 * 2) + 3

			val = (b0 << 24) + (b1 << 16) + (b2 << 8) + b3

			print('Bytes: ' + str([b0,b1,b2,b3]))

			print('Decimal: ' + str(val))

			print('Hex: ' + hex(val))
