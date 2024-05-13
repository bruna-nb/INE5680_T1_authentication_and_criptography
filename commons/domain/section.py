class Section:

    def __init__(self, username, totp_code, status):
        self.username = username
        self.totp_code = totp_code
        self.status = status

    def set_username(self, username):
        self.username = username

    def set_totp_code(self, totp_code):
        self.totp_code = totp_code

    def set_status(self, status):
        self.status = status

    def get_username(self):
        return self.username

    def get_totp_code(self):
        return self.totp_code

    def get_status(self):
        return self.status