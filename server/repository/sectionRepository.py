from commons.utils.loggerUtils import LoggerUtils
import sqlite3

class SectionRepository:
    
    LOGGER = LoggerUtils.get_logger("SECTION_REPOSITORY")

    def __init__(self):
        self.set_up_section_repository()

    def set_up_section_repository(self):
        self.conn = sqlite3.connect('messenger.db')
        def trace_callback(query):
            self.LOGGER.debug(f'Executando operacao no banco de dados: {query}')
        self.conn.set_trace_callback(trace_callback)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS section
                (username TEXT NOT NULL, totp_code INTEGER NOT NULL, status TEXT NOT NULL)''')
        
    def get_totp_code_by_username_and_status(self, username:str, status:str) -> int:
        self.c.execute("SELECT totp_code FROM section WHERE username=? AND status=?",(username,status,))
        return int(self.c.fetchone()[0])
    
    def save_section(self, username:str, totp_code:int, status:str):
        self.c.execute("INSERT INTO section (username, totp_code, status) VALUES (?, ?, ?)",(username, totp_code, status))
        self.conn.commit()

    def update_section_status(self, username:str, totp_code:int, status:str):
        self.c.execute("UPDATE section SET status = ? WHERE username = ? AND totp_code = ?", (status, username, totp_code))
        self.conn.commit()
    