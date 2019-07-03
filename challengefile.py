import base64
from cryptography.fernet import Fernet
from _datetime import datetime
from random import *

import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
pin_provided = "9834" # This is input in the form of a string
pin = pin_provided.encode() # Convert to type bytes
# Time Factor and random number
time_factor=str(datetime.now())
time_factor_str=''.join(e for e in time_factor if e.isalnum())
time_factor_int=int(time_factor_str)
random_number=randint(10000,100000000)
# Challenge
challenge_int= time_factor_int+random_number
# convert challenge to type bytes
challenge_bytes=str(challenge_int).encode()
#instance of PBKDF2HMAC
backend = default_backend()
# salt is randomly generated
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=backend
)
# key will now have the value of a url safe base64 encoded key
key = base64.urlsafe_b64encode(kdf.derive(pin))
#Encrypting the challenge
f = Fernet(key)
encrypted = f.encrypt(challenge_bytes)
hashed_challenge = abs(hash(encrypted))