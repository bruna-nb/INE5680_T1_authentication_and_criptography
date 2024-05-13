from commons.utils.loggerUtils import LoggerUtils
from commons.utils.encryptUtils import EncryptUtils
from commons.domain.user import User
from commons.domain.message import Message
from server.serverInterface import ServerInterface
from datetime import datetime
import sys

LOGGER = LoggerUtils.get_logger("CLIENT_INTERFACE")
encrypt_utils = EncryptUtils()
server_interface = ServerInterface()
logged_user:User = None
simetric_key = None

def login():
    username = input("Informe o nome de usuário: ")
    LOGGER.debug(f'Usuario efetuando login: {username}')

    user_salt = server_interface.get_salt_by_username(username)
    LOGGER.debug(f'Salt encontrado para o usuario {username}: {str(user_salt)}')
    if user_salt == None:
        print("\nUsuário não encontrado. Tente novamente.\n")
        return

    password = input(f'Informe a senha para o usuário {username}: ')
    authentication_token = encrypt_utils.get_pbkdf2_encrypt(password, user_salt)
    LOGGER.debug(f'Token de autenticacao: {authentication_token}')

    user = User(username, authentication_token)
    totp = server_interface.login(user, datetime.now())
    if  totp != None:
        LOGGER.debug(f'Codigo totp para o usuario {username}: {totp.now()}')
        totp_code = int(input("\nVerificação de identidade. Informe o código TOTP: "))
        #alterar validação do codigo TOTP para o server
        if server_interface.validate_2fa(totp, totp_code, username):
            print("verificado")
            global logged_user
            logged_user = user
            LOGGER.debug(f'Usuario logado: {logged_user.get_username()}')
            #Após login, derivar chave simetrica da sessão
            user_salt = server_interface.get_salt_by_username(username)
            global simetric_key
            simetric_key = encrypt_utils.get_scrypt_encrypt( str(totp_code), user_salt)
            LOGGER.debug(f'Chave simetrica gerada para secao de {username}: {simetric_key}')
            return user_menu()
        
    return
        
def user_menu():
    print("Menu de usuario")
    value = 0
    while value > -1 :
        value = int(input("Selecione uma opção: \n" + 
                       "0: Enviar mensagem \n" + 
                       "-1: Sair \n"))
        if value == 0:
            global simetric_key
            message = input("Digite sua mensagem")
            message = encrypt_utils.encrypt_message(message, simetric_key)
            print("Enviando mensagem ao servidor")
            LOGGER.debug(f'mensagem encriptada {message}')
            server_response = server_interface.receive_message(Message(logged_user.get_username(), "USER", message))
            process_server_response(server_response)            
    pass

def process_server_response(message: Message):
    global simetric_key
    LOGGER.debug(f'Recebida mensagem criptografada: {message.get_content()}')
    decripted_message = encrypt_utils.decrypt_message(message.get_content(), simetric_key)
    LOGGER.debug(f'Mensagem decriptada: {decripted_message}')


def create_user():
    username = input("Informe o novo nome de usuário: ")
    password = input(f'Informe uma nova senha para o usuário {username}: ')
    salt = encrypt_utils.generate_salt()
    user = User(username, encrypt_utils.get_pbkdf2_encrypt(password, salt))
    if server_interface.create_user(user, salt):
        LOGGER.debug(f'Novo usuario criado. User = {user.get_username()}, encrypted password = {user.get_password()}.')
        print("\nUsuário criado com sucesso!\n")
    else:
        print("\nUsuário já existe com esse username. Tente novamente.\n")

def get_user_option():
    LOGGER.debug("Usuario deve escolher entre login(1) ou criacao de novo usuario(2).")
    option = int(input("Selecione uma opção: \n" + 
                       "1: Fazer login \n" + 
                       "2: Cadastrar novo usuário \n" +
                       "0: SAIR \n"))
    
    LOGGER.debug(f'Opcao digitada pelo usuario: {option}')
    
    if option == 0:
        LOGGER.debug("Encerrando aplicacao.")
        sys.exit()
    
    if option != 1 and option != 2:
        print("\nOpção invalida. Tente novamente.\n")
        return get_user_option()  

    return option  

while True:
    option = get_user_option()

    if option == 1:
        login()
    else:
        create_user()