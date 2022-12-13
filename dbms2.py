# работа с таблицей Users
import hashlib
import mysql.connector
import random


class User :
    def __init__( self, cursor = None ) -> None :
        if cursor == None :
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
            row = cursor.fetchone()
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
        sql = f"INSERT INTO Users VALUES( UUID(), %s, '{user.passw}', %s, '{user.salt}', %s, %s, '{user.email_code}', 0 )"
        try :
            cursor = self.db.cursor()
            cursor.execute( sql, ( user.login, user.name, user.avatar, user.email ) )
            cursor.commit()
        except mysql.connector.Error as err :
            print( err ) 
            return False
        else :
            return True
        finally :
            cursor.close()


def main() -> None :
    user = User()
    user.login = "admin"
    user.passw = "123"
    user.name = "Root Administrator"
    user.avatar = None
    user.email = "admin@ukr.net"

    userDao = UserDAO()
    print( userDao.add_user( user ) )


if __name__ == "__main__" :
    main()

# Д.З. (добавление пользователя) Реализовать открытие подключения к БД, передать его
# в UserDAO, выполнить запрос на добавление нового пользователя. Проверить успешность из консоли БД
# ** Реализовать передачу в main() не только подключения, но и объекта userDao


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
'''