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

    def auth_user( self, login:str, password:str ) -> User | None :
        user = self.get_user( login = login )
        if user : 
            hash_pass = hashlib.sha1( ( user.salt + password ).encode() ).hexdigest()
            if hash_pass == user.passw :
                return user
        return None

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
