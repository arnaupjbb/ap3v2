from yogi import *
from sys import *
import time


start = time.time() 

def find_best_sol_rec(ce, ne, quant, mill_clas, used, sol, dislike, best_cost, idx, lasts2) -> int :
    C, M, K = len(sol), len(mill_clas[0]), len(used)
    addp = 0
    
    if dislike +addp >= best_cost : return best_cost

    
    
    if idx == C :
        for m in range(M):
            for i in range(idx-2, max(idx - ne[m], -1), -1):
                addp += max(0, lasts2[m][idx-1] - lasts2[m][i-1] - ce[m])
        dislike += addp   
        if dislike < best_cost:
            best_cost = dislike
            with open(argv[1],"w") as f: 
                endi = time.time()
                print(best_cost, round(endi - start,1), file=f)
                print(' '.join(map(str, sol)), file=f)
        return best_cost
    else :
        for k in range(K) :
            if used[k] < quant[k]:
                sol[idx] = k
                used[k] += 1
                pen = 0
                for m in range(M):
                    lasts2[m][idx] = lasts2[m][idx-1]
                    if mill_clas[k][m]: lasts2[m][idx] += 1
                    mp = lasts2[m][idx]
                    if idx >= ne[m]:
                        mp -= lasts2[m][idx - ne[m]]
                    if mp > ce[m]:
                        pen += mp - ce[m]
                
                best_cost = find_best_sol_rec(ce, ne, quant, mill_clas, used, sol, dislike + pen,best_cost, idx + 1, lasts2)
                used[k] -= 1
        return best_cost

def read_prob() -> tuple[int, int, int, list[int], list[int], list[int], list[list[bool]]]:
    """Llegeix el problema i retorna totes les dades de l'entrada"""
    C, M, K = read(int), read(int), read(int)
    ce = [read(int) for _ in range(M)]  # quantitat que podem fer
    ne = [read(int) for _ in range(M)]  # per cada ne cotxes
    
    quant = []                          # cotxes de cada classe
    mill_clas = [[] for _ in range(K)]  # la classe i requereix la millora j?

    for i in range(K):
        read(int)
        quant.append(read(int))
        for _ in range(M):
            mill_clas[i].append(bool(read(int)))
    return C, M, K, ce, ne, quant, mill_clas


def main():
    C, M, K, ce, ne, quant, mill_clas = read_prob()
    sol = [-1]*C # place person with index 0 at the first position
    idx = 0 # next position to fill in sol
    dislike = 0 # dislike of sol (partial solution)
    used = [0]*K
    best_cost = C*C*M
    lasts2 = [[0 for _ in range(C)] for _ in range(M)] #Cada fila es una millora, cada columna l'index
    cost = find_best_sol_rec(ce, ne, quant, mill_clas, used, sol, dislike, best_cost, idx, lasts2)


    
main()