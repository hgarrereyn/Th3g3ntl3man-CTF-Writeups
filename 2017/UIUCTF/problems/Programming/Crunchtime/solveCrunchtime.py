# By Harrison Green <hgarrereyn>

from pwn import *

import base64, zlib
import numpy as np

# ===== Variables and functions provided by encodeTones.py

sample_rate = 44100
number_of_digits = 11

tone_samples = int(0.3*sample_rate)
tone_time = np.linspace(0, tone_samples/sample_rate, tone_samples, endpoint=False)
lower_band = np.array([697, 770, 852, 941])
upper_band = np.array([1209, 1336, 1477, 1633])

tone_ordering = np.array([['1','2','3','A'],['4','5','6','B'],['7','8','9','C'],['E','0','F','D']])

def output_decode(b64_string):
    return np.fromstring(zlib.decompress(base64.b64decode(b64_string)), dtype=np.float64)

# ===== End provided

# This takes a numpy array and returns the 11 character hexstring
def decode_val(data):
	# hexstring
	s = ''

	for i in range(number_of_digits):
		# these define the section of the array to check
		tone_start = i * tone_samples
		tone_end = tone_start + tone_samples

		# section of the array that corresponds to exactly one character
		dat = data[tone_start:tone_end]

		# perform a fourier transform on the data and calculate
		# the frequencies from the nuber of samples
		fft = np.fft.fft(dat)
		freq = np.fft.fftfreq(tone_samples)

		# Define a threshold and find the peaks of the fft plot.
		#
		# Then mask the frequencies array to determine which frequencies
		# those peaks correspond to.
		thresh = 0.75 * max(abs(fft))
		mask = abs(fft) > thresh
		peaks = freq[mask] * sample_rate

		# The fft function is working with imaginary numbers while we only
		# provided real float values. Therefore, it will return both positive
		# and negative frequencies corresponding to clockwise and counter-clockwise
		# waveforms.
		#
		# We just select the positive frequencies
		tones = peaks[np.where(peaks > 0)]

		# determine the lower tone and the higher tone (of the two frequencies
		# that we found)
		lower_tone = min(tones)
		higher_tone = max(tones)

		# Sometimes the frequencies won't be perfect so we just need to find
		# the closest match for each frequency and use that index.
		tone_index = (np.abs(lower_band - lower_tone).argmin(), np.abs(upper_band - higher_tone).argmin())

		# calculate the hex character
		val = tone_ordering[tone_index]

		# append to string
		s += val

	return s


# open the connection
sock = remote('challenge.uiuc.tf', 11341)

print('Verification...')

raw = sock.recvline()
data = output_decode(raw[2:-1]) # strip away enclosing characters
s = decode_val(data)
sock.sendline(s)

print('Getting flag...')

flag = ""

while True:
	raw = sock.recvline()
	if (!raw):
		break

	data = output_decode(raw[2:-1])
	s = decode_val(data)
	sock.sendline(s)

	print('Got chunk: ' + s)
	flag += s

print('Flag: ' + flag)
