from server.repository.userRepository import UserRepository
from commons.utils.loggerUtils import LoggerUtils
from commons.domain.user import User
from commons.utils.encryptUtils import EncryptUtils
from commons.utils.authenticationUtils import AuthenticationUtils
from datetime import datetime

class ServerInterface:
    
    LOGGER = LoggerUtils.get_logger("SERVER_INTERFACE")
    user_repository = UserRepository()
    encrypt_utils = EncryptUtils()
    authentication_utils = AuthenticationUtils()

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

