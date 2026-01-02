from yogi import *
import time
from sys import *


def greedy(
        C: int, M: int, K:int, ce: list[int], ne: list[int], 
        quant: list[int], mill_clas: list[list[bool]], pens:list[int]
        ) -> tuple[int, list[int]]:
    
    """Donat un problema, generem una solució més o menys propera a un òptim amb un algorisme golafre.
    Per triar entre una classe i una altra prioritza: menor penalització que afegeix a la seqüència actual, 
    major quantitat de cotxes restants, major quantitat de suma de cotxes a afegir per les seves millores (val)
    i menor nombre de millores requerides"""
    act_sol: list[int] = []
    act_pen: int = 0
    used: list[int] = [0]*K 
    rem: list[int] = [0]*M  # Guarda quants cotxes queden per la millora m
    lasts: list[int] = [0]*M # Guarda quants cotxes amb la millora m tenim per l'última finestra de llargada ne[m]
   
    
    for m in range(M):
        for k in range(K):
            rem[m] += (quant[k]-used[k])*int(mill_clas[k][m])
    
    for i in range(C):

        # Creem variables per guardar la millor penalizació fins al moment amb la seva classe, 
        next_pen = C*C*M 
        next_k = 0
        # Enter que guardarà la suma de quants cotxes queden per les millores que requereix la millor classe
        next_val = -1
        for k in range(K):
            if used[k] < quant[k] :
                # Càlcul de penalitzacions i val
                pos_pen = 0
                val = 0
                for m in range(M):
                    mlas = lasts[m]
                    if mill_clas[k][m]:
                        mlas += 1
                        val += rem[m]
                        
                    if i >= ne[m] and mill_clas[act_sol[i-ne[m]]][m]:
                        mlas -= 1
                    if mlas > ce[m]:
                        pos_pen += mlas - ce[m]
                if ((pos_pen, used[k]-quant[k], -val, pens[k]) < 
                        (next_pen, used[next_k]-quant[next_k], -next_val, pens[next_k])):
                    # Triem entre la classe a explorar i la millor trobada i actualitzem
                    next_pen = pos_pen
                    next_k  = k
                    next_val = val

        # Actualitzem valors
        used[next_k] += 1
        for m in range(M):
            if mill_clas[next_k][m]:
                rem[m] -= 1
                lasts[m] += 1
            if i >= ne[m] and mill_clas[act_sol[-ne[m]]][m]:
                lasts[m] -= 1
        act_sol.append(next_k)
        act_pen += next_pen

    # Afegim penalització final   
    for m in range(M):
        count = 0
        for i in range(C-1, max(C - ne[m], -1), -1):
            if mill_clas[act_sol[i]][m]:
                count += 1
            if count > ce[m]:
                act_pen += count - ce[m]

    return act_pen, act_sol
            

def read_prob() -> tuple[int, int, int, list[int], list[int], list[int], list[list[bool]], list[int]]:
    """Reads the problem and returns its data"""
    C, M, K = read(int), read(int), read(int)
    ce = [read(int) for _ in range(M)]  # quantitat que podem fer
    ne = [read(int) for _ in range(M)]  # per cada ne cotxes
    pens = [0]*K
    quant = []                          # cotxes de cada classe
    mill_clas = [[] for _ in range(K)]  # la classe i requereix la millora j?

    for i in range(K):
        read(int)
        quant.append(read(int))
        for _ in range(M):
            have = bool(read(int))
            mill_clas[i].append(have)
            if have:
                pens[i] += 1
    return C, M, K, ce, ne, quant, mill_clas, pens



def main():
    start = time.time()
    C, M, K, ce, ne, quant, mill_clas, pens = read_prob()
    
    best_pen, best_sol = greedy(
        C, M, K, ce, ne, quant, mill_clas, pens
        )
    with open(argv[1],"w") as f: 
        endi = time.time()
        print(best_pen, round(endi - start,1), file=f)
        print(' '.join(map(str, best_sol)), file=f)

if __name__ == "__main__":
    main()
