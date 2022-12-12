# подключение к БД с использованием MariaDB коннектора
# https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/

import mariadb         # pip3 install mariadb

def main( pars ) :
    try :
        connection = mariadb.connect( **pars )
    except mariadb.Error as err :
        print( err )
    else :
        print( "Connection OK" )
    return


if __name__ == "__main__" :
    pars = {
        "host":     "localhost",
        "port":     3306,
        "database": "py1911",
        "user":     "py191_user",
        "password": "pass_191",
    }
    main( pars )   # ~иньекция - точка внедрения общих параметров
