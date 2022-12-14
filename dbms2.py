# работа с таблицей Users
import hashlib
import mysql.connector
import random
import uuid


class User :
    def __init__( self, row = None ) -> None :
        if row == None :
            self.id         = ''
            self.login      = '' 
            self.passw      = '' 
            self.name       = '' 
            self.salt       = '' 
            self.avatar     = '' 
            self.email      = '' 
            self.email_code = '' 
            self.email_code_attempts = '' 
        else :
            if row :
                self.id         = row[0]
                self.login      = row[1]
                self.passw      = row[2] 
                self.name       = row[3]
                self.salt       = row[4]
                self.avatar     = row[5]
                self.email      = row[6]
                self.email_code = row[7]
                self.email_code_attempts = row[8]


class UserDAO :
    def __init__( self, db: mysql.connector.MySQLConnection ) -> None:
        self.db = db

    def add_user( self, user : User ) -> bool :
        ''' Appends user to DB table '''
        # предполагаем, что в поле passw приходит открытый пароль, генерируем хеш здесь
        user.salt = random.randbytes( 20 ).hex()
        user.passw = hashlib.sha1( ( user.salt + user.passw ).encode() ).hexdigest()
        # генерируем код подтверждения почты
        user.email_code = random.randbytes( 3 ).hex()
        # user.__dict__ - словарь с собственными полями объекта (рефлексия)
        # задача: сформировать запрос к БД используя все поля объекта user
        # 1. для запроса нужен перечень полей (имена через запятую) - fields
        #     + заменить имя passw (user) на pass (db)
        # 2. для значений нужен перечень именованных подстановок '%(name)s' (через запятую) - placeholders
        user.id = str( uuid.uuid4() )
        user.email_code_attempts = 0
        # print( user.__dict__ )
        names = user.__dict__.keys()
        fields = ','.join( f"`{name}`" for name in names ).replace( 'passw', 'pass' )   # `id`,`login`,`name`, ...
        placeholders = ','.join( f"%({name})s" for name in names )
        sql = f"INSERT INTO Users({fields}) VALUES({placeholders})"
        # print( sql )
        # sql = f"INSERT INTO Users VALUES( UUID(), %s, '{user.passw}', %s, '{user.salt}', %s, %s, '{user.email_code}', 0 )"
        try :
            cursor = self.db.cursor()
            # cursor.execute( sql, ( user.login, user.name, user.avatar, user.email ) )
            cursor.execute( sql, user.__dict__ )  # подстановка значений именованных параметров
            self.db.commit()
        except mysql.connector.Error as err :
            print( err ) 
            return False
        else :
            return True
        finally :
            cursor.close()

    def get_users( self ) -> tuple | None :
        try :
            cursor = self.db.cursor()
            cursor.execute( "SELECT * FROM users" ) 
        except mysql.connector.Error as err :
            print( 'get_users:', err ) 
            return None
        else :
            return tuple( User( row ) for row in cursor )
        finally :
            cursor.close()
        return
# Д.З. Реализовать вывод списка пользователей в удобном для просмотра виде
# вместо (<__main__.User object at 0x00000158D263D910>, <__main__.User object at 0x00000158D261F810>)


def main( db: mysql.connector.MySQLConnection ) -> None :
    # user = User()
    # user.login = "admin"
    # user.passw = "123"
    # user.name = "Root Administrator"
    # user.avatar = None
    # user.email = "admin@ukr.net"
    # user.login = "user"
    # user.passw = "123"
    # user.name = "Experienced User"
    # user.avatar = None
    # user.email = "user@ukr.net"

    userDao = UserDAO( db )
    # print( userDao.add_user( user ) )
    print( userDao.get_users() )


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
    try :
        connection = mysql.connector.connect( **pars )
    except mysql.connector.Error as err :
        print( "Connection:", err )
        exit()
    else :
        main( connection )   # точка инъекции
    finally :
        connection.close()



'''
CREATE TABLE `users` (
  `id`                  char(36)    NOT NULL       COMMENT 'UUID',
  `login`               varchar(32) NOT NULL,
  `pass`                char(40)    NOT NULL       COMMENT 'SHA-160 hash',
  `name`                tinytext    NOT NULL,
  `salt`                char(40)    DEFAULT NULL   COMMENT 'SHA-160 of random',
  `avatar`              varchar(64) DEFAULT NULL   COMMENT 'Avatar filename',
  `email`               varchar(64) DEFAULT NULL   COMMENT 'User E-mail',
  `email_code`          char(6)     DEFAULT NULL   COMMENT 'E-mail confirm code',
  `email_code_attempts` int(11)     DEFAULT 0      COMMENT 'Count of invalid E-mail confirmations',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;


Python              ~socket              DBMS
db.cursor() <-------------------------->
cur.execute(sql) -----(SELECT)---------> PLAN - схема выполнения
cur.fetchone()  -----------------------> получение одной строки (одно выполнение PLAN)
                <----------------------- отправка рез-та


Python              ~socket              DBMS
db.cursor() <-------------------------->
cur.execute(sql) -----(SELECT)---------> PLAN - схема выполнения + выполнение несколько раз
                        (буфер)<-------- для заполнения буфера     
cur.fetchone()  ----->(буфер)                  
               <------ получение одной строки 
                        (буфер) <------- Если опустошается, то заполнить

Подготовленный запрос
Python              ~socket              DBMS
db.cursor() <-------------------------->
                подготовка запроса
cur.prepare(sql) -----(SELECT ?)-------> PLAN - схема выполнения (создается временная хранимая процедура с параметром)
                выполнение запроса
cur.execute(data1) -----(data1)--------> выполнение (EXEC) хранимой процедуры с аргументом data1
cur.fetchone()  -----------------------> получение одной строки (одно выполнение PLAN)
                <----------------------- отправка рез-та
         повторное выполнение не посылает повторного SQL (SELECT)
cur.execute(data2) -----(data2)--------> выполнение (EXEC) хранимой процедуры с аргументом data2
cur.fetchone()  -----------------------> получение одной строки (одно выполнение PLAN)
                <----------------------- отправка рез-та
         возможно многократное выполнение       
cur.close()    ------------------------> разрушение временной процедуры

Транзакция
Python              ~socket              DBMS
db.cursor() <-------------------------->
cur.query("CREATE TRANSACTION") -------> Начало транзакции (присваивается id транзакции)
cur.query(sql1)                          на время транзакции каждая команда сохраняет
cur.query(sql2)                          предыдущее состояние для возможности отмены транзакции
cur.query(sql3)                          а также блокирует таблицу/строки для других запросов (не из этой транзакции)
cur.query("COMMIT TRANSACTION") -------> конец транзакции
                       либо
cur.query("ROLLBACK TRANSACTION") -----> отмена транзакции

'''