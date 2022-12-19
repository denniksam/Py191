#!C:/Python311/python.exe

import os, sys
import urllib.parse   # url encoder/decoder

# метод запроса 
method = os.environ["REQUEST_METHOD"]

# URL-параметры (Query String) доступны в переменной QUERY_STRING
query_string = urllib.parse.unquote( os.environ["QUERY_STRING"] )
# задание: разобрать в словарь
params = dict( param.split("=", maxsplit=1) if '=' in param else (param, None)
    for param in query_string.split("&") if param != '')

# заголовки - переносим в словарь
headers = dict( ((k[5:] if k.startswith( 'HTTP_' ) else k).lower(), v)
    for k,v in os.environ.items() 
        if k.startswith( 'HTTP_' ) 
            or k in [ "CONTENT_LENGTH", "CONTENT_TYPE" ] )


# тело запроса передается в контекст sys.stdin
body = sys.stdin.read()
# Д.З. Проверить заголовок  Content-Type, если он application/json, то
# попробовать "разобрать" тело как json, в случае ошибок вернуть информацию
# об ошибке, иначе - разобранный словарь


# Режим backend (API) - машинно-машинное взаимодействие, при котором не 
# передается человеко-понятный HTML, а используются машино-понятные данные
print( "Content-Type: text/plain; charset=cp1251" )
print( "" )  # пустая строка, отделяющая тело
print( method )
print( os.environ["QUERY_STRING"], query_string, params )
print( headers )
print( body, end='' )  # print добавляет \n из-за чего возможны искажения данных
