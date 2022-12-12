# Работа с БД. Основы

'''
0. СУБД. Установить MySQL/MariaDB
    а) отдельным ПО (скачать, распаковать - готово к работе)
    б) в составе "сборок" - XAMPP, OpenServer, Danver
    в) в составе Workbench (инструментов БД)
1. Создаем БД, а также пользователя для нее.
    !! не рекомендуется использовать администратора root для 
    всех задач, желательно создавать отдельных пользователей
    - открываем терминал БД / инструмент (Workbench)
        mysql -u root    (mysql -u root -p)
    - создаем новую БД (py191)
        CREATE DATABASE py191 ;
    - создаем пользователя (py191_user / pass_191)
        CREATE USER py191_user@localhost IDENTIFIED BY 'pass_191' ;
    - даем пользователю права на одну БД
        GRANT ALL PRIVILEGES ON py191.* TO py191_user@localhost ;
        FLUSH PRIVILEGES ;
    Проверяем:
        Отключаемся от БД  как root:    exit
        Заходим как новый пользователь: mysql -u py191_user -p
                                        Enter password: ******** (pass_191)
        Должны попасть в СУБД
        Проверяем доступность БД:  
            SHOW DATABASES ; - в перечне должна быть py191

2. Драйверы подключения: коннекторы.
    Коннекторы подбираются под БД и ПО (MySQL-Python)
    Рекомендуется искать драйверы от производителя БД
    https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html
    (продолжение - в dbms_my1.py)
    https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
    (продолжение - в dbms_ma1.py)

'''
