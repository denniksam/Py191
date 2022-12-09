# работа с JSON
import json          # модуль работы с JSON, стандартный, входит в Python

def main() :
    try :
        with open( "sample.json" ) as f :
            j = json.load( f )
    except :
        print( "JSON load or parse error" )
        return
    print( type(j), j )           # <class dict>
    print( "------------------------------" )
    for k in j :                  # итерирование dict - проход по ключам первого уровня, в глубину не сканнирует
        print( k, j[k],           # j[k] - доступ к значению по ключу
            type( j[k] ) )        # типы разные, соответствуют значениям (123-int, 12.34-float, ...)
    print( "------------------------------" )
    for v in j.values() :         # цикл по значениям, ключи игнорируются
        print( v )                # проход по первому уровню, в глубину не сканнирует
    print( "------------------------------" )
    for k,v in j.items() :        # комбинированный цикл - и ключи, и значения
        print( k, ':', v )
    print( "------------------------------" )
    j["newItem1"] = "New item 1"  # расширение коллекции (словаря) новым значением
    j["d"] = 321                  # существующий ключ - изменение данных
    j["newItem2"] = "Привет"      # non-ASCII символы экранируются в JSON ("\u041f\u0440\u0438\u0432\u0435\u0442" )
    print(                        # dumps  ~ stringify / serialize / encode - строка с JSON представлением
        json.dumps( j,            # объект сериализации
            indent = 4,           # pretty-print печать с отступами и через строки
            ensure_ascii = False  # не экранировать non-ASCII символы
    ) )
    try :
        with open( "sample2.json", "w" ) as f :
            json.dump( j, f )     # dump (no -s) - запись в файл
    except :
        print( "File write error" )
    else :
        print( "File write OK" ) 
    


if __name__ == "__main__" :
    main()
