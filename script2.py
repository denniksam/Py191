# Типизация - динамическая, но при записи: переменная получает тип после присваивания
# и сохраняет его до следующего присваивания.
#
x = "12"
# print( x + 1 )       # TypeError: can only concatenate str (not "int") to str
print( x + str(1) )    # 121
print( int(x) + 1 )    # 13

x = 12                 # после присваивания тип переменной меняется
print( x + 1 )
# print( x + str(1) )  # TypeError: unsupported operand type(s) for +: 'int' and 'str'
print( int(x) + 1 )

x = int( input( "Введите х = " ) )
if x < 10 :
    print( "x < 10" )
elif x < 20 :
    print( "10 - 20" )
elif x < 30 :
    print( "20 - 30" )
else :
    print( "other" )

if x > 10 and x < 20 :
    print( "10..20" )
elif x > 20 or x < 10 :
    print( "<10 or >20" )


