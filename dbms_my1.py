# подключение к БД с использованием MySQL коннектора
# https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html

import mysql.connector       # pip install mysql-connector-python
import random

def insert_data( connection: mysql.connector.MySQLConnection ) :
    sql = "INSERT INTO tests(num, ukr, str) VALUES(%s, %s, %s)"
    alf = "абвгдеєжзиіїклмнопрстуфхцчшщьюя" 
    str = ''.join( [ random.choice(alf) for i in range( random.choice([3,4]) ) ] )
    cursor = connection.cursor() 
    try :
        # cursor.execute( (sql), ( ( random.randint(10, 20), "їжак", "їжак" ) ) )
        cursor.execute( (sql), ( ( random.randint(10, 20), str, str ) ) )
        connection.commit()   # буферизация запросов / транзакция -- отправка накопленных изменений (~flush)
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
        ukr VARCHAR(128)  COLLATE utf8_unicode_ci ,
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


def show_data( connection: mysql.connector.MySQLConnection, order="G" ) -> None :
    ''' Shows data from 'tests' table ordering by 'order' value: 'G' - general (default), 'U' - unicode '''
    sql = "SELECT * FROM tests t ORDER BY " + ( 't.ukr' if order == 'U' else 't.str' )
    try :
        cursor = connection.cursor()
        cursor.execute( sql )         # выполнение команды создает в БД правило получения данных, но сами данные не передает
    except mysql.connector.Error as err :
        print( err )
    else :                            # передача данных из БД происходит по командам чтения (fetch) либо итерирования cursor
        # for row in cursor :         # после читающего запроса сам cursor становится итерируемым
        #     print( row )  
        print( cursor.column_names )  # данные об именах полей
        while True :                  # аналог предыдущего цикла в раскрытой форме
            row = cursor.fetchone()   # явная команда чтения одной записи (строки результата запроса)
            if row == None :
                break
            print( row )        
    finally :
        try : cursor.close()          # возможно исключение "Unread result found" если не все данные будут запрошены
        except : pass
    return


def select_dict( connection: mysql.connector.MySQLConnection, order="G" ) -> tuple :
    sql = "SELECT * FROM tests t ORDER BY " + ( 't.ukr' if order == 'U' else 't.str' )
    try :
        cursor = connection.cursor()
        cursor.execute( sql ) 
    except mysql.connector.Error as err :
        print( err )
    else :
        res = ( 
            dict( ( k, v ) for k, v in zip( cursor.column_names, vals ) ) 
            for vals in cursor )
    # vals = ('013a9b43-7a25-11ed-adf5-14857fd97497', 11, 'їжак', 'їжак')
    # res = dict( ( k, v ) for k, v in zip( names, vals ) )
    return res


def main( pars ) :
    try :
        connection = mysql.connector.connect( **pars )
    except mysql.connector.Error as err :
        print( "Connection:", err )
        return
    else :
        print( "Connection OK" )

    # create_table( connection )
    # insert_data( connection )
    # show_data( connection )
    # show_data( connection, order='U' )
    # print( select_dict( connection, order='U' ) )
    for row in select_dict( connection, order='U' ) :
        print( row['num'], row['ukr'] )    # доступ к полям по именам + частичная выборка (не все отображаем)

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
