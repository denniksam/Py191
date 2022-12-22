#!C:/Python311/python.exe

# API аутентификации
import os, sys
import base64

def send401( message:str = None ) -> None :
    print( "Status: 401 Unauthorized" )
    if message : print( "Content-Type: text/plain" )
    print()
    if message : print( message, end='' )
    return


auth_header = None
if 'HTTP_AUTHORIZATION' in os.environ.keys() :
    auth_header = os.environ['HTTP_AUTHORIZATION']
elif 'REDIRECT_HTTP_AUTHORIZATION' in os.environ.keys() :
    auth_header = os.environ['REDIRECT_HTTP_AUTHORIZATION']

# Проверяем наличие заголовка Authorization
if not auth_header :
    send401( "Authorization header required" )
    exit()

# Проверяем схему авторизации Basic
if not auth_header.startswith( 'Basic' ) :
    send401( "Basic Authorization header required" )
    exit()

# декодируем переданную строку
try :
    cred = base64.b64decode( auth_header[6:], validate=True ).decode( 'utf-8' )
except :
    send401( "Malformed credentials: Login:Password base64 encoded expected" )
    exit()

# Проверяем формат строки (должен быть ":")
if not ':' in cred :
    send401( "Malformed credentials: Login:Password base64 encoded required" )
    exit()

# Разделяем логин и пароль по первому ":" (в пароле могут быть свои ":")
user_login, user_password = cred.split( ':', maxsplit = 1 )

# подключаем БД: создали файлы-модули db.py(conf) dao.py(User,UserDAO)
sys.path.append( "../" )  # доп. папка для поиска модулей
import db
import dao
import mysql.connector

try :
    con = mysql.connector.connect( **db.conf )
except :
    send401( "Internal Error" )
    exit()

# получаем пользователя по логину и паролю
user = dao.UserDAO(con).auth_user( user_login, user_password )
if not user :
    send401( "Credentials rejected" )
    exit()

# генерируем токен для пользователя
access_token = dao.AccessTokenDAO( con ).create( user )
if not access_token :
    send401( "Token creation error" )
    exit()

print( "Status: 200 OK" )
print( "Content-Type: application/json; charset=UTF-8" )
print( "Cache-Control: no-store" )
print( "Pragma: no-cache" )
print()
print( f'''{{
    "access_token": "{access_token.token}",
    "token_type": "Bearer",
    "expires_in": "{access_token.expires}"
}}''', end='' )


'''
Токены - данные, позволяющие идентифицировать подключение. Чаще всего это строки, бывают
бинарные данные, бывают JWT (JSON данные).
Для ведения токенов организуются отдельные таблицы (БД). Токен принадлежит определенному
пользователю и имеет ограниченный срок действия:
 от пересоздания для каждого запроса
 до практически бессрочного интервала (год и более)
Бывает, что различные токены принадлежат одному пользователю но отвечают за различные права
 (например, github)
CREATE TABLE access_tokens (
    token    CHAR(40)  PRIMARY KEY,
    user_id  CHAR(36)  NOT NULL,
    expires  DATETIME  NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB, DEFAULT CHARSET=UTF8
'''

#Д.З. Проверить заголовок Authorization на валидность (наличие разделенных ":" логина и пароля)
# Схема: пользователь обращается на /auth, передает логин и пароль
# Authorization: Basic <логин:пароль в кодировке base64>
# Если заголовка нет, то выдаем 401
# Проверяем логин, пароль и генерируем токен
# по стандарту https://datatracker.ietf.org/doc/html/rfc6750 (page 9)
# токен передается в теле ответа
#      Content-Type: application/json;charset=UTF-8
#      Cache-Control: no-store
#      Pragma: no-cache
#      {
#        "access_token":"mF_9.B5f-4.1JqM",
#        "token_type":"Bearer",
#        "expires_in":3600,
#        "refresh_token":"tGzv3JOkF0XG5Qx2TlKWIA"
#      }
# base64 - транспортная кодировка для передачи произвольных данных в канале,
# поддерживающем 64 разрешенных символа: 10 цифр, 26+26 алфавит + 2 доп. символа
# (разные для разных стандартов, классика "-=", URL "-_"). Идея
#  - исходные данные записываются в бинарном виде (последовательность бит)
#  - последовательность разбивается по 6 бит
#  - каждые 6 бит заменяются на символ (один из 64-х) 
#  - поскольку 8n бит не всегда делится на 6, то добавляются символы выравнивания (=)