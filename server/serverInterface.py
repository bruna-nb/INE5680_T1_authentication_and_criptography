from server.repository.userRepository import UserRepository
from server.repository.sectionRepository import SectionRepository
from commons.utils.loggerUtils import LoggerUtils
from commons.domain.user import User
from commons.utils.encryptUtils import EncryptUtils
from commons.utils.authenticationUtils import AuthenticationUtils
from commons.domain.message import Message
from datetime import datetime
from pyotp import TOTP

class ServerInterface:
    
    LOGGER = LoggerUtils.get_logger("SERVER_INTERFACE")
    user_repository = UserRepository()
    encrypt_utils = EncryptUtils()
    authentication_utils = AuthenticationUtils()
    section_repository = SectionRepository()

    def get_salt_by_username(self, username:str):
        db_result = self.user_repository.get_salt_by_username(username)
        if db_result == None or len(db_result) == 0:
            return None
        return db_result[0]
       
    def get_user_by_username(self, username:str) -> User:
        db_result = self.user_repository.get_user_by_username(username)
        if db_result == None or len(db_result) == 0:
            return None
        return User(db_result[0], db_result[1])
    
    def login(self, user:User, timestamp:datetime):
        user_password = self.get_user_by_username(user.get_username()).get_password()
        salt = self.get_salt_by_username(user.get_username())
        scrypt_password = self.encrypt_utils.get_scrypt_encrypt(user.get_password(), salt)

        if scrypt_password == user_password and ((datetime.now() - timestamp).total_seconds() < 45):
            return self.authentication_utils.generate_2fa_code()
        else:
            self.LOGGER.debug(f'Usuario ou senha incorretos. Retornando para o menu principal.')
            print("\nUsuário ou senha incorretos.\n")
            return None
    
    def create_user(self, user:User, salt:str):
        try:
            existing_user = self.get_user_by_username(user.get_username())
            if existing_user != None:
                self.LOGGER.debug(existing_user)
                self.LOGGER.debug(f'Usuario {user.get_username()} nao pode ser criado porque ja existe na base.')
                return False
            scrypt_password = self.encrypt_utils.get_scrypt_encrypt(user.get_password(), salt)
            self.user_repository.save_user(user.get_username(), scrypt_password, salt)
            return True
        except Exception as e:
            self.LOGGER.error(f'Erro ao criar usuario. {e.args}')
            return False
        
    def validate_2fa(self, totp:TOTP, totp_code_input:int, username:str):
        if(totp.verify(totp_code_input)):
            self.create_section(totp_code_input, username, "ACTIVE")
            return True
        return False
    

    def create_section(self, totp_code:int, username:str, status:str):
        self.section_repository.save_section(username, totp_code, status)

    def receive_message(self, message: Message):
        self.LOGGER.debug(f'Recebida mensagem criptografada: {message.get_content()}')
        totp_code = str(self.section_repository.get_totp_code_by_username_and_status(message.get_username(), "ACTIVE"))
        salt = self.get_salt_by_username(message.get_username())
        key = self.get_section_key(totp_code, salt)

        decripted_message = self.encrypt_utils.decrypt_message(message.get_content(), key)
        self.LOGGER.debug(f'Mensagem decriptada: {decripted_message}')

        return self.send_user_message(message.get_username(), key)

    def send_user_message(self, username, key):
        mensagem = input("Digite uma mensagem para enviar ao usuário: ")
        content = self.encrypt_utils.encrypt_message(mensagem, key)
        print("Enviando mensagem ao usuário")
        return Message(username, "SERVER",content)

    def get_section_key(self, code, salt):
        return self.encrypt_utils.get_scrypt_encrypt(code, salt)


    

