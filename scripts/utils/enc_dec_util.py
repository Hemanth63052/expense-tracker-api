from cryptography.fernet import Fernet
from scripts.config import ENCRY_DECRY_CONF


class EncrDecUtil:
    def __init__(self):
        self.key = ENCRY_DECRY_CONF.FERNET_KEY
        self.cipher = Fernet(self.key)

    def encrypt_password(self, password):
        encrypted_password = self.cipher.encrypt(password.encode())
        return encrypted_password

    def decrypt_password(self, encrypted_password):
        decrypted_password = self.cipher.decrypt(encrypted_password)
        return decrypted_password.decode()
