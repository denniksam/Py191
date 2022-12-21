#!C:/Python311/python.exe

# API, требующий авторизации. Признак авторизации - наличие заголовка Authorization
import os

auth_header = None
if 'HTTP_AUTHORIZATION' in os.environ.keys() :
    auth_header = os.environ['HTTP_AUTHORIZATION']
elif 'REDIRECT_HTTP_AUTHORIZATION' in os.environ.keys() :
    auth_header = os.environ['REDIRECT_HTTP_AUTHORIZATION']

if not auth_header :
    print( "Status: 401 Unauthorized" )
    # print( f'WWW-Authenticate: Bearer realm="Get token on /auth "' )
    print()
    exit()

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
