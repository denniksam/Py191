# работа с таблицей Users
import hashlib
import mysql.connector
import random
import uuid


class User :
    def __init__( self, row = None ) -> None :
        if row == None :
            self.id         = None
            self.login      = None 
            self.passw      = None 
            self.name       = None 
            self.salt       = None 
            self.avatar     = None 
            self.email      = None 
            self.email_code = None 
            self.email_code_attempts = None
            self.del_dt     = None
        elif isinstance( row, tuple ) :
            self.id         = row[0]
            self.login      = row[1]
            self.passw      = row[2] 
            self.name       = row[3]
            self.salt       = row[4]
            self.avatar     = row[5]
            self.email      = row[6]
            self.email_code = row[7]
            self.email_code_attempts = row[8]
            self.del_dt     = row[9]
        elif isinstance( row, dict ) :
            self.id         = row["id"]
            self.login      = row["login"]
            self.passw      = row["pass"] 
            self.name       = row["name"]
            self.salt       = row["salt"]
            self.avatar     = row["avatar"]
            self.email      = row["email"]
            self.email_code = row["email_code"]
            self.email_code_attempts = row["email_code_attempts"]
            self.del_dt     = row["del_dt"]
        else :
            raise ValueError( "row format unsupported" )

    def __str__( self ) -> str :
        return str( self.__dict__ )

    # def __repr__(self) -> str:
    #     return self.__str__()
    __repr__ = __str__


class UserDAO :
    def __init__( self, db: mysql.connector.MySQLConnection ) -> None :
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

    def get_users( self, ignore_deleted = True ) -> tuple | None :
        sql = "SELECT * FROM users"
        if ignore_deleted :
            sql += " WHERE del_dt IS NULL"
        try :
            cursor = self.db.cursor( dictionary = True )
            cursor.execute( sql ) 
        except mysql.connector.Error as err :
            print( 'get_users:', err ) 
            return None
        else :
            return tuple( User( row ) for row in cursor )
        finally :
            cursor.close()
        return
# Д.З. Реализовать метод is_login_free( login : str ), учесть тот факт,
# что за удаленными пользователями логины все равно закреплены и есть занятыми (можно делегировать get_user())
# Реализовать метод auth_user(login:str, passw:str) -> User | None

    # задание: добавить пар-р ignore_deleted = True, учесть его
    def get_user( self, id = None, login = None ) -> User | None :
        sql = "SELECT u.* FROM Users u WHERE "
        params = []
        if id :
            sql += "u.id = %s "
            params.append( id )
        if login :
            sql += ( "AND " if id else "" ) + "u.login = %s"
            params.append( login )
        if len( params ) == 0 :
            return None

        try :
            cursor = self.db.cursor( dictionary = True )
            cursor.execute( sql, params )
            row = cursor.fetchone()
            if row :
                return User( row )
        except mysql.connector.Error as err :
            print( 'get_user:', err )
        finally :
            try : cursor.close()
            except : pass
        return None

    def update( self, user : User ) -> bool :
        ''' Обновление данных о пользователе. user.id используется как ключ, остальные поля
            обновляют значения в БД. !!! Если меняется пароль получить хеш нужно до вызова метода'''
        # задание: подготовить текст запроса в виде            остальные поля user
        # UPDATE users u SET u.`login`=%(login)s, u.`pass`=%(passw)s, ... WHERE u.`id`=%(id)s
        sql = 'UPDATE users u SET ' + \
            ','.join( f"u.`{x.replace('passw','pass')}`=%({x})s" for x in user.__dict__.keys() if x != 'id' ) + \
            ' WHERE u.`id`=%(id)s'
        # print( sql )
        try :
            cursor = self.db.cursor()
            cursor.execute( sql, user.__dict__ )  # подстановка значений именованных параметров
            self.db.commit()
        except mysql.connector.Error as err :
            print( err ) 
            return False
        else :
            return True
        finally :
            try : cursor.close()
            except : pass

    def delete( self, user : User ) -> bool :
        '''Удаление пользователя - это не удаление записи из БД, это установка поля del_dt'''
        if not user : return False
        try :
            cursor = self.db.cursor()
            cursor.execute( "UPDATE users u SET u.del_dt = CURRENT_TIMESTAMP WHERE u.id = %s", (user.id,) ) 
            self.db.commit()
        except mysql.connector.Error as err :
            print( err ) 
            return False
        else :
            return True
        finally :
            try : cursor.close()
            except : pass

    

def main( db: mysql.connector.MySQLConnection ) -> None :
    # user = User()
    # user.login = "moder"
    # user.passw = "123"
    # user.name = "Post Moderator"
    # user.avatar = None
    # user.email = "moder@ukr.net"
    # user.login = "user"
    # user.passw = "123"
    # user.name = "Experienced User"
    # user.avatar = None
    # user.email = "user@ukr.net"

    userDao = UserDAO( db )
    # print( userDao.add_user( user ) )
    print( userDao.get_users() )
    print( userDao.get_users( ignore_deleted=False ) )
    # print( userDao.get_user( id = '953daa4e-6df3-4d5c-8c4a-75bca62bb151' ) )
    # print( userDao.get_user( id = '!953daa4e-6df3-4d5c-8c4a-75bca62bb151' ) )
    # print( userDao.get_user( login = 'admin' ) )
    # print( userDao.get_user( login = 'nobody' ) )
    # user = userDao.get_user( login = 'moder' ) ; print( user ) 
    # print( userDao.delete( user ) )
    # user.email = "admin@gmail.com"
    # print( userDao.update( user ) )


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
Традиционно для удаления сущностей в таблицах закладывают доп. поля типа is_deleted (bool) либо
del_dt(datetime) момент удаления. В более сложных системах ведется журнал удалений: кто-что-когда-коммент
ALTER TABLE users ADD COLUMN IF NOT EXISTS del_dt DATETIME DEFAULT NULL ;

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