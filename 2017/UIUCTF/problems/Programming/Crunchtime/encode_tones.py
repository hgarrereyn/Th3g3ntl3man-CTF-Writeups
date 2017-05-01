import numpy as np
from flag import hexflag
from random import choice
import string
import base64
import zlib

sample_rate = 44100
number_of_digits = 11

tone_samples = int(0.3*sample_rate)
tone_time = np.linspace(0, tone_samples/sample_rate, tone_samples, endpoint=False)
lower_band = np.array([697, 770, 852, 941])
upper_band = np.array([1209, 1336, 1477, 1633])

[lower_band, upper_band] = np.meshgrid(upper_band, lower_band)

tone_ordering = np.array([['1','2','3','A'],['4','5','6','B'],['7','8','9','C'],['E','0','F','D']])

def find_character_index_tuple(character):
    inter = np.where(tone_ordering==character)
    return (inter[0][0], inter[1][0])

def encode_hex_string_as_dtmf(hexstring):
    if(len(hexstring) != number_of_digits):
        print("You lied to me!")
        exit(-1)

    master_indices = []
    for char in hexstring:
        master_indices.append(find_character_index_tuple(char))

    encoded = np.zeros(tone_samples * number_of_digits, dtype=np.float64)

    for i in range(number_of_digits):
        tone_start = i*tone_samples
        tone_end = (i+1)*tone_samples
        indices = master_indices[i]
        encoded[tone_start:tone_end] += 0.5*np.sin(2*np.pi*lower_band[indices[0],indices[1]]*tone_time + np.random.uniform(0,2*np.pi))
        encoded[tone_start:tone_end] +=  0.5*np.sin(2*np.pi*upper_band[indices[0],indices[1]]*tone_time + np.random.uniform(0,2*np.pi))

    return encoded

def generate_random_hex_string():
    out = ""
    hexchars = [char for char in string.digits + "ABCDEF"]
    for i in range(number_of_digits):
        out += choice(hexchars)
    return out

def do_challenge(output_function, soln_input_function):
    for _ in range(number_of_digits):
        k = generate_random_hex_string()
        data = encode_hex_string_as_dtmf(k)

        output_function(data)
        solve = soln_input_function()

        if(solve != k):
            print("You came so far...")
            exit(0)

def chunks(l, n):
    """http://stackoverflow.com/a/312464"""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def encode_flag(output_function, soln_input_function):
    for part in chunks(hexflag, number_of_digits):
        data = encode_hex_string_as_dtmf(part)
        output_function(data)

        solve = soln_input_function()

        if(solve != part):
            print("You messed up *now*???")

def output_encode(np_array):
    return base64.b64encode(zlib.compress(np_array.tostring(), 9))

def output_decode(b64_string):
    return np.fromstring(zlib.decompress(base64.b64decode(b64_string)), dtype=np.float64)

if (__name__ == '__main__'):
    do_challenge(lambda q : print(output_encode(q)), input)
    encode_flag(lambda q : print(output_encode(q)), input)
