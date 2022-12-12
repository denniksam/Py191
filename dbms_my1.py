# подключение к БД с использованием MySQL коннектора
# https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html

import mysql.connector       # pip install mysql-connector-python

def insert_data( connection: mysql.connector.MySQLConnection ) :
    sql = "INSERT INTO tests(num, ukr, str) VALUES(%s, %s, %s)"
    cursor = connection.cursor() 
    try :
        cursor.execute( (sql), ( 10, "Їжак", "Їжак" ) )
        connection.commit()
    except  mysql.connector.Error as err :
        print( "INSERT:", err )
    else :
        print( "INSERT OK" )
    finally :
        cursor.close()
    return


def create_table( connection: mysql.connector.MySQLConnection ) :
    ''' Creates table tests '''
    sql = ''' CREATE TABLE tests (
        id  CHAR(36)  PRIMARY KEY  DEFAULT UUID() ,
        num INT,
        ukr VARCHAR(128)  COLLATE cp1251_ukrainian_ci,
        str VARCHAR(128)  COLLATE utf8_general_ci
    ) Engine = InnoDB, DEFAULT CHARSET = UTF8
    '''
    cursor = connection.cursor()   # ~Statement/SqlCommand
    try :
        cursor.execute( sql )
    except  mysql.connector.Error as err :
        print( "CREATE:", err )
    else :
        print( "CREATE OK" )
    finally :
        cursor.close()
    return


def main( pars ) :
    try :
        connection = mysql.connector.connect( **pars )
    except mysql.connector.Error as err :
        print( "Connection:", err )
        return
    else :
        print( "Connection OK" )

    # create_table( connection )
    insert_data( connection )
    return


if __name__ == "__main__" :
    pars = {
        "host":     "localhost",
        "port":     3306,
        "database": "py191",
        "user":     "py191_user",
        "password": "pass_191",
        
        "charset":  "utf8mb4",
        "use_unicode": True,
        "collation": "utf8mb4_general_ci"
    }
    main( pars )   # ~иньекция - точка внедрения общих параметров

''' Д.З. Написать инструкцию для генерирования случайной строки
(3-4 случайных символа Укр. алфавита) для запроса к БД '''
