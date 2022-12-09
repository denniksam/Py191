# lambda - выражения

def main() :
    lam1 = lambda x : print( x )
    lam1( "Hello" )
    lam2 = lambda x, y : print( x, y )
    lam2( "Hello", "World" )
    lam3 = lambda : print( "No args" )
    lam3()
    (lambda:print("1"))()    # IIFE - выражения мгновенного вызова
    

if __name__ == "__main__" :
    main()
