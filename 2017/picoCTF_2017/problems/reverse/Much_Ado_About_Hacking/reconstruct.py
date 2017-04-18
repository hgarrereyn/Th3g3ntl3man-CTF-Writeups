# By Harrison Green <hgarrereyn>

# The output we want to recreate
out = raw_input()

# Get the output values
outVal = [ord(x) for x in out]

# The memory operator (initially zero)
b = 0

# Initialize a new array the size of the output string
c = [0] * len(out)

for i in range(0, len(out)):
	# First pass and disassociate from memory operator
	c[i] = outVal[i] - 32 - b

	# Reverse the mod function by assuming that inputs were in
	# range [0,192)
	if c[i] < 0:
		c[i] = c[i] + 96

	# Memory storage
	b = c[i]

	# Final pass
	c[i] = c[i] + 32

# Reverse array and convert back to string
in_str = "".join([chr(x) for x in c][::-1])

# Print
print(in_str)
