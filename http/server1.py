import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class MainHandler( BaseHTTPRequestHandler ) :
    def do_GET( self ) -> None :
        print( self.path )                        # вывод в консоль (не в ответ сервера)
        path_parts = self.path.split( "/" )       # разделенный на части запрос, path_parts[0] - пустой, т.к. path начинается со "/" 
        if path_parts[1] == "" :
            path_parts[1] = "index.html"
        # print( os.getcwd() )
        fname = "./http/" + path_parts[1]
        if os.path.isfile( fname ) :              # запрос - существующий файл
            # print( fname, "file" )
            self.flush_file( fname )
        elif path_parts[1] == "auth" :            # запрос - /auth
            self.auth()
        else :
            # print( fname, "not file" )
            self.send_response( 200 )
            self.send_header( "Content-Type", "text/html" )
            self.end_headers()
            self.wfile.write( "<h1>404</h1>".encode() )
        return

    def log_request(self, code: int | str = ..., size: int | str = ...) -> None:
        '''Метод, выводящий в консоль данные о запросе'''
        # return super().log_request(code, size)
        return

    def flush_file( self, filename ) -> None :
        # Определить расширение файла filename
        ext = filename.split(".")[-1]

        # Установить Content-Type согласно расширению
        if ext in ('png', 'bmp') :
            content_type = "image/" + ext
        elif ext == 'ico' : 
            content_type = "image/x-icon"
        elif ext == 'html' : 
            content_type = "text/html"
        else :
            content_type = "application/octet-stream"

        self.send_response( 200 )
        self.send_header( "Content-Type", content_type )
        self.end_headers()
        # Передать файл в ответ
        with open( filename, "rb" ) as f :
            self.wfile.write( f.read() )
        return

    def auth( self ) :   # API
        # Проверяем наличие заголовка Authorization
        auth_header = self.headers.get( "Authorization" ) 
        if auth_header is None :
            self.send_401( "Authorization header required" )
            return
        # Проверяем схему авторизации Basic
        if not auth_header.startswith( 'Basic' ) :
            self.send_401( "Basic Authorization header required" )
            return
        # декодируем переданную строку
        try :
            cred = base64.b64decode( auth_header[6:], validate=True ).decode( 'utf-8' )
        except :
            self.send_401( "Malformed credentials: Login:Password base64 encoded expected" )
            return        
        # Проверяем формат строки (должен быть ":")
        if not ':' in cred :
            self.send_401( "Malformed credentials: Login:Password base64 encoded required" )
            return

        # Разделяем логин и пароль по первому ":" (в пароле могут быть свои ":")
        user_login, user_password = cred.split( ':', maxsplit = 1 )    

        self.send_response( 200 )
        self.send_header( "Content-Type", "text/html" )
        self.end_headers()
        self.wfile.write( (user_login + user_password).encode() )
        return
    # Д.З. Реализовать "глубокий" поиск файлов: создать папки css, js
    # поместить в них файлы style.css, script.js с демонстрационным действием.
    # В главном index.html подключить стиль и скрипт
    # Обеспечить правильную работу подключаемых файлов

    def send_401( self, message = None ) :
        self.send_response( 401 )
        self.send_header( "Status", "401 Unauthorized" )
        if message : self.send_header( "Content-Type", "text/plain" )
        self.end_headers()
        if message : self.wfile.write( message.encode() )


def main() -> None :
    http_server = HTTPServer( ( '127.0.0.1', 88 ), MainHandler )
    try :
        print( "Server started" )
        http_server.serve_forever()
    except :
        print( "Server stopped" )


if __name__ == "__main__" :
    main()

'''
Другой способ органиции сервера - собственный сервер с обработчиком запросов
Инструменты - в модуле http.server
 HTTPServer - класс для запуска сервера
 BaseHTTPRequestHandler - родительский класс для обработчиков запросов

Особенности:
 обработчик запросов определяет методы do_GET, do_POST, ...
   вместо параметров метода определяются поля/методы класса для работы с запросом/ответом
 вызов print выводит данные в консоль запуска скрипта, для передачи данных в ответ
   нужен вызов спец. методов 
 все запросы заданным методом попадают в обработчик, запросы к файлам автоматически
   не прорабатываются. Передачу всех файлов необходимо прописывать в обработчике
   Также не прорабатывается маршрутизация: /items/phones/123 также ведет просто к do_GET
 для тела ответа предоставляется self.wfile. в который в бинарном виде записываются
   данные 

self.path - строка запроса. Из нее нужно выделить имя файла и проверить на то, что этот
   файл существует. Если есть - передать как ответ

'''