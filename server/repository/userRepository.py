from commons.utils.loggerUtils import LoggerUtils
from commons.domain.user import User
import sqlite3

class UserRepository:
    
    LOGGER = LoggerUtils.get_logger("USER_REPOSITORY")

    def __init__(self):
        self.set_up_users_repository()

    def set_up_users_repository(self):
        self.conn = sqlite3.connect('messenger.db')
        def trace_callback(query):
            self.LOGGER.debug(f'Executando operacao no banco de dados: {query}')
        self.conn.set_trace_callback(trace_callback)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS users
                (username TEXT NOT NULL, password TEXT NOT NULL, salt TEXT NOT NULL)''')
        
    def get_salt_by_username(self, username) -> str:
        self.c.execute("SELECT salt FROM users WHERE username=?",(username,))
        return self.c.fetchone()
    
    def get_user_by_username(self, username):
        self.c.execute("SELECT * FROM users WHERE username=?",(username,))
        return self.c.fetchone()
    
    def save_user(self, username:str, password:str, salt:str):
        self.c.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",(username, password, salt))
        self.conn.commit()
    


