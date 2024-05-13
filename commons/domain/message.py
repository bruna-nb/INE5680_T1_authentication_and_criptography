class Message:
    
    def __init__(self, username:str, origin:str, content:str):
        self.username = username
        self.origin = origin
        self.content = content

    def set_username(self, username:str):
        self.username = username

    def set_origin(self, origin:str):
        self.origin = origin
    
    def set_content(self, content:str):
        self.content = content

    def get_username(self):
        return self.username
    
    def get_origin(self):
        return self.origin
    
    def get_content(self):
        return self.content