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
'''  
    def encrypt_message(self, message, key):
        # Padding da mensagem para ser um múltiplo de 16 bytes (tamanho do bloco AES)
        if len(message) % 16 != 0:
            message += ' ' * (16 - len(message) % 16)
        
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.iv + cipher.encrypt(message.encode('utf-8'))
        return ciphertext
    
    def decrypt_message(self, encrypted_message, key):
        iv = encrypted_message[:16]  # O IV é o primeiro bloco do texto cifrado
        ciphertext = encrypted_message[16:]  # O restante é o texto cifrado
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext).rstrip(b' ')
        return plaintext.decode('utf-8')
''' 