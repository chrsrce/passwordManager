# Password Generation and Hash Tools

import hashlib
import random
import string

# "Constants"
# Use these instead of hard-coded literals for easier maintenance.
USER_USERNAME_MIN_LENGTH = 4
USER_PASSWORD_MIN_LENGTH = 4
PLATFORM_PASSWORD_LENGTH = 32
SALT_LENGTH = 16

# Converts a list to a string.
def list_to_string(list):
	string = ""

	for i in list:
		string += i
	
	return string

# Generates a random string of given length, consisting of digits, letters, and punctuation.
# Can be used to generate either passwords or salts.
def random_string(length):
	return list_to_string(random.choices(string.digits + string.ascii_letters + string.punctuation, k = length))

# Generates a SHA256 hash from given plaintext and salt.
def salted_hash(plaintext, salt):
	return hashlib.sha256((salt + plaintext).encode()).hexdigest()