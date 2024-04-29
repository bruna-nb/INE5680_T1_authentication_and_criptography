from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
import os

class EncryptUtils:

    def generate_salt(self):
        return os.urandom(16)
    
    def get_pbkdf2_encrypt(self, password, salt):
        return PBKDF2(password, salt, 16, 1000, None, SHA512)
    
    def get_scrypt_encrypt(self, password, salt):
        return scrypt(password, salt, 32, N=2**14, r=8, p=1)