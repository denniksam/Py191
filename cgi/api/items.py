#!C:/Python311/python.exe

# API, требующий авторизации. Признак авторизации - наличие заголовка Authorization
import os, sys

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

# Проверяем схему авторизации Bearer
if not auth_header.startswith( 'Bearer' ) :
    send401( "Bearer Authorization header required" )
    exit()

# Извлекаем токен
access_token = auth_header[7:]   # убираем 'Bearer' + space

# Проверяем токен
sys.path.append( "../" )  # доп. папка для поиска модулей
import db
import dao
import mysql.connector

try :
    con = mysql.connector.connect( **db.conf )
except :
    send401( "Internal Error" )
    exit()

token = dao.AccessTokenDAO( con ).get( access_token )
if not token :
    send401( "Token rejected" )
    exit()

# Проверяем активность токена (срок)



print( "Status: 200 OK" )
print( "Content-Type: text/plain" )
print()
print( "Secret items coming soon", end='' )

# """
# Схема:
#  пользователь запрашивает /items
#  если он не авторизован, то выдается код 401
#  пользователь должен обратиться на /auth, передать логин/пароль, получить токен
#  далее используя токен снова обращается к  /items, токен проверяется и выдается ответ
# """
