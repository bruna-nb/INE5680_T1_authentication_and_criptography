import os
import base64
from pyotp import TOTP

class AuthenticationUtils:

    def generate_2fa_code(self):
        totp = TOTP(base64.b32encode(os.urandom(20)).decode("utf-8"))
        return totp