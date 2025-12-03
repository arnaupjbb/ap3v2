from yogi import *
from sys import *
import time


start = time.time()

def lowbound(ce, ne, mill_clas, quant, used, idx, C, remaining, sol):
    st = time.time()
    min_pen = 0
    M, K = len(ne), len(quant)
    for m in range(M):
        nwin = (C-idx)//ne[m]
        cap = ce[m]*nwin + ce[m]
        if remaining[m] > cap: min_pen += ne[m]*(remaining[m] - cap)
    return min_pen


def find_best_sol_rec(ce: list[int], ne: list[int], quant: list[int], 
                    mill_clas: list[list[bool]], used: list[int], sol: list[int],
                    act_pen: int, best_cost: int, idx: int, lasts: list[int], addprox, remaining) -> int :
    
    C, M, K = len(sol), len(mill_clas[0]), len(used)
    if act_pen + addprox + lowbound(ce, ne, mill_clas, quant, used, idx, C, remaining, sol) >= best_cost : return best_cost

    if idx == C :
        for m in range(M):
            count = 0
            for i in range(C-1, max(C - ne[m], -1), -1):
                if mill_clas[sol[i]][m]:
                    count += 1
                if count > ce[m]:
                    act_pen += count - ce[m]
                if act_pen >= best_cost: return best_cost
                
                
        if act_pen < best_cost:
            best_cost = act_pen
            with open(argv[1],"w") as f: 
                endi = time.time()
                print(best_cost, round(endi - start,1), file=f)
                print(' '.join(map(str, sol)), file=f)
        return best_cost
    else :
        for k in range(K) :
            if used[k] < quant[k]:
                addprox = 0
                sol[idx] = k
                used[k] += 1
                pen = 0
                for m in range(M):
                    if mill_clas[k][m]: 
                        lasts[m] += 1
                        remaining[m] -= 1
                    if idx >= ne[m] and mill_clas[sol[idx - ne[m]]][m]: lasts[m] -= 1
                    if lasts[m] > ce[m]:
                        pen += lasts[m] - ce[m]
                        addprox += (lasts[m] - ce[m])*(lasts[m] - ce[m]-1)//2
                
                best_cost = find_best_sol_rec(ce, ne, quant, mill_clas, used, sol, act_pen + pen,best_cost, idx + 1, lasts, addprox, remaining) 
                
                for m in range(M):
                    if mill_clas[k][m]: 
                        lasts[m] -= 1
                        remaining[m] += 1
                    if idx >= ne[m] and mill_clas[sol[idx - ne[m]]][m]: lasts[m] += 1
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
    sol = [-1]*C
    idx = 0 
    act_pen = 0 
    used = [0]*K
    best_cost = C*C*M
    lasts = [0]*M
    remaining = [0]*M
    for m in range(M):
        for k in range(K):
            if mill_clas[k][m]:
                remaining[m] += quant[k]
    cost = find_best_sol_rec(ce, ne, quant, mill_clas, used, sol, act_pen, best_cost, idx, lasts, 0, remaining)
    print(time.time()-start)
    
main()