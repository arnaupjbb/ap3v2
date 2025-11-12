from yogi import *
from sys import *
import time

def main ( ) :
    start = time.time() 
    # Llegim dades del canal estàndar d'entrada
    a = read(int)
    b = read(int)

    # escrivim a l'arxiu indicat en el primer argument de la línia de comandes
    arch = argv[1]
    with open(arch,"w") as f:    
        for i in range(a*a*a):
            if i%(a*a) == 0:
                print(i, file=f)
    end = time.time() 
    with open(arch,"w") as f: 
        print(end - start,file=f)


main()

