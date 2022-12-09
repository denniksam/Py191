# работа с файлами

def write_file1() :
    try :
        f = open( "file1.txt", mode = "w", encoding="utf-8" )
        f.write( "Hello from file\n" )
        f.write( "Next Line " )
        f.flush()
        f.close()
    except OSError as err :   # ~ IOException
        print( "File write error:", err.strerror )


def write_file2() :  # блок with ( ~using/try() ) - работа с ресурсами
    try :            # окончание блока автоматически освобождает ресурс
        with open( "file2.txt", mode = "w", encoding="utf-8" ) as f :
            f.write( "Hello from file\n" )
            f.write( "Next Line " )
    except OSError as err :
        print( "File write error:", err.strerror )


def file_get_contents( name ) -> str | None :
    try :
        f = open( name, mode = "r", encoding="utf-8" )
        return f.read()
    except FileNotFoundError as err :
        print( "File open error:", err.strerror )
    finally :
        if f != None : 
            f.close()
        else :
            return None


def read_lines1() -> None :
    '''Prints file by lines preceding line numbers'''
    try :
        with open( "file1.txt" ) as f :
            n = 0
            for line in f.readlines() :   # \n сохраняется в line
                n += 1                    # n++, ++n не реализованы
                print( n, line,  end = '' )
    except OSError as err :
        print( 'read_lines1:', err )



def main() :
    # write_file2(); return    
    # print( file_get_contents( "file1.txt" ) )
    read_lines1()

if __name__ == "__main__" :
    main()

''' 
    Д.З. Создать файл, имитирующий заголовки HTTP, например
        Host: localhost
        Connection: close
        Content-Type: text/html
        Content-Length: 100500
    реализовать чтение этого файла, разбор заголовков в dict
'''