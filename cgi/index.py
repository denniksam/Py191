#!C:/Python311/python.exe

import os
# os.environ - переменные окружения
envs = "<ul>" + ''.join( f"<li>{k} = {v}</li>" for k,v in os.environ.items() ) + "</ul>"

print( "Content-Type: text/html; charset=utf-8" )
print( "" )   # empty line
print( f"""<!doctype html />
<html>
<head>
    <title>Py-191</title>
</head>
<body>
{__name__}
    <h1>Hello CGI World!</h1>
    {envs}
</body>
</html>""" )
# Домашнее задание: вывести  значения только следующих переменных окружения:
# REQUEST_METHOD , QUERY_STRING , REQUEST_URI , REMOTE_ADDR , REQUEST_SCHEME 