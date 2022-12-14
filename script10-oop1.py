# основы ООП

class MyClass :                  # Описание класса    
    x = 10                       # поле в классе - статическое и public
                                 #   
                                 #    
def main() -> None :             #   
    obj1 = MyClass()             # создание объекта: особенность без new
    obj2 = MyClass()             # 
    print( obj1.x, obj2.x )      # (10,10) - оба поля обращаются к одному стат. полю  
    MyClass.x = 15               # изменение значения в статическом поле
    print( obj1.x, obj2.x )      # (15,15) - оба объекта ссылаются на одно поле
    obj1.x = 20                  # динамическая типизация позволяет создавать поля на лету
    obj2.y = 30                  #  свои поля имеют приоритет при конфликте имен
    print( obj1.x, obj2.x )      # (20,15) obj1.x - объектный, obj2.x - статический (свой - у)
    del obj2.y                   # разрушение объектного поля у


if __name__ == "__main__" :
    main()
