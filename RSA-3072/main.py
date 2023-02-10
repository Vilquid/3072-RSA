import random
import sys


sys.setrecursionlimit(1000000)  # Increase the recursion limit for large primes


# Implement the extended Euclidean algorithm
def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	g, y, x = egcd(b % a, a)
	return (g, x - (b // a) * y, y)


# Implement the modular inverse function
def modinv(a, m):
	g, x, y = egcd(a, m)
	if g != 1:
		raise Exception("No modular inverse")
	return x % m


# Implement the Miller-Rabin primality test
def is_probably_prime(n, k=5):
	if n <= 1 or n == 4:
		return False
	if n <= 3:
		return True
	d = n - 1
	s = 0
	while d % 2 == 0:
		d //= 2
		s += 1
	for i in range(k):
		a = random.randint(2, n - 2)
		x = pow(a, d, n)
		if x == 1 or x == n - 1:
			continue
		for r in range(s - 1):
			x = pow(x, 2, n)
			if x == n - 1:
				break
		else:
			return False
	return True


# Implement the Miller-Rabin primality generation
def generate_prime(bits):
	while True:
		p = random.getrandbits(bits)
		if is_probably_prime(p):
			return p


# Implement the RSA key generation
def generate_keypair(bits):
	p = generate_prime(bits // 2)
	q = generate_prime(bits // 2)
	n = p * q
	phi = (p - 1) * (q - 1)
	e = random.randrange(1, phi)
	g, _, y = egcd(e, phi)
	while g != 1:
		e = random.randrange(1, phi)
		g, _, y = egcd(e, phi)
	d = modinv(e, phi)
	return (e, n), (d, n)


# Implement the RSA encryption
def encrypt(plaintext, public_key):
	key, n = public_key
	cipher = [pow(ord(char), key, n) for char in plaintext]
	return cipher


# Implement the RSA decryption
def decrypt(ciphertext, private_key):
	key, n = private_key
	plain = [chr(pow(char, key, n)) for char in ciphertext]
	return ''.join(plain)


# Example usage:
message = "The quick brown fox jumps over the lazy dog."
print("Original message:", message)

# Generate the public and private keys
public_key, private_key = generate_keypair(3072)
print("Public key: ", public_key)
print("Private key: ", private_key)

encrypted = encrypt(message, public_key)
print("Encrypted message:", encrypted)

decrypted = decrypt(encrypted, private_key)
print("Decrypted message:", decrypted)
