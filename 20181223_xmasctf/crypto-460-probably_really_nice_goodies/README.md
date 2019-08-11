# X-MAS CTF 2018: Probably Really Nice Goodies (Crypto 460)

__Tags:__ `xor`, `LFSR`  
__Total Points:__ 460    
__Toal Solvers:__ 31


## Problem Statement

You are given a ciphertext and a python code that encrypted it.

```python
import os

flag = open('flag.txt').read().strip()

class PRNG():
	def __init__(self):
		self.seed = self.getseed()
		self.iv = int(bin(self.seed)[2:].zfill(64)[0:32], 2)
		self.key = int(bin(self.seed)[2:].zfill(64)[32:64], 2)
		self.mask = int(bin(self.seed)[2:].zfill(64)[64:96], 2)
		self.aux = 0

	def parity(self,x):
		x ^= x >> 16
		x ^= x >> 8
		x ^= x>> 4
		x ^= x>> 2
		x ^= x>> 1
		return x & 1

	def getseed(self):
		return int(os.urandom(12).encode('hex'), 16)

	def LFSR(self):
		return self.iv >> 1 | (self.parity(self.iv&self.key) << 32)

	def next(self):
		self.aux, self.iv = self.iv, self.LFSR()

	def next_byte(self):
		x = self.iv ^ self.mask
		self.next()
		x ^= x >> 16
		x ^= x >> 8
		return (x & 255)

def encrypt(s):
	o=''
	for x in s:
		o += chr(ord(x) ^ p.next_byte())
	return o.encode('hex')

p=PRNG()

with open('flag.enc','w') as f:
	f.write(encrypt(flag))
```

## Solution

Here we look at the psuedorandom number generator, and we treat the `LSFR` component as a blackbox since we cannot reliably find any weaknesses there. Where we can look i at is the `next_byte(.)` function.

```python
def next_byte(self):
    x = self.iv ^ self.mask
    # self.next()
    self.iv = self.LFSR()
    x ^= x >> 16
    x ^= x >> 8
    return (x & 255)
```

Where `self.LFSR()` shifts the IV to the right by 1 bit and generates a random bit on the left most bit.

Notice here that __the mask simply xors the IV__, and we can actually simplify this function with some 8 bit `mask_prime` which is the overall effect of mask on the output.

```python
def next_byte(self):
    x = self.iv
    self.iv = self.LFSR()
    x ^= x >> 16
    x ^= x >> 8
    return (x & 255) ^ self.mask_prime
```

Similarly, we can also simplify this further by getting the overall effect of `LSFR` on the output, which is `LFSR_prime` which is now only a linear feedback shift register 8 bits long.

```python
def next_byte(self):
    ret = self.x
    self.x = self.LFSR_prime()
    return x ^ self.mask_prime
```

From here, it is easy to show that the relationship between two consecutive outputs of `next_byte(.)` is constant.

```
prev = x ^ mask_prime
curr = ((x >> 1)| random_8th_bit) ^ mask_prime

(prev >> 1) = (x >> 1) ^ (mask_prime >> 1)
curr & 127  = (x >> 1) ^ (mask_prime & 127)

_mask = (prev >> 1) ^ (curr & 127)
      = (mask_prime >> 1) ^ (mask_prime & 127)
```

`_mask` is trivial to get because the first few bytes the plaintext should be `X-MAS{` and, if we know this `_mask`,and the current output of `next_byte(.)`, __we can predict all of the bits of the next output, except for the most significant bit__.

But note that since the flag is printable, then all the plaintext bytes should be less than 127, which means that __the most significant bit of the plaintext should always be 0__.

With all that, we can easily derive sequence of bytes generated by `next_byte(.)`.

This gives us the flag `X-MAS{S4n7a_4lw4ys_g1ve5_n1c3_pr3s3n7s}`
## Implementation

```python
def get_mask(prev, curr):
	ret = (prev>>1)^curr
	return (ret & 127)

with open('flag.enc') as f:
	flag = bytearray.fromhex(f.read())

#flag format X-MAS{...}
# Getting the first two random bytes
mask = get_mask(flag[0]^ord('X'), flag[1]^ord('-'))


prev = flag[0]^ord('X')
pt = ['X']
for e in flag[1:]:
	curr = (prev >> 1) ^ mask ^ e
	if curr > 127:
		curr ^= 128
	pt.append(chr(curr))
	prev = e^curr

print(''.join(pt))

```