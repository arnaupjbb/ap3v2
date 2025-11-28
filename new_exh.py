from yogi import *
from sys import *
import time


start = time.time()

def find_best_sol_rec(ce: list[int], ne: list[int], quant: list[int], 
                    mill_clas: list[list[bool]], used: list[int], sol: list[int],
                    act_pen: int, best_cost: int, idx: int, lasts: list[int]) -> int :
    
    C, M, K = len(sol), len(mill_clas[0]), len(used)
    if act_pen >= best_cost : return best_cost

    if idx == C :
        for m in range(M):
            count = 0
            for i in range(C-1, max(C - ne[m], -1), -1):
                if mill_clas[sol[i]][m]:
                    count += 1
                if count > ce[m]:
                    act_pen += count - ce[m]
                
                
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
                sol[idx] = k
                used[k] += 1
                pen = 0
                for m in range(M):
                    if mill_clas[k][m]: lasts[m] += 1
                    if idx >= ne[m] and mill_clas[sol[idx - ne[m]]][m]: lasts[m] -= 1
                    if lasts[m] > ce[m]:
                        pen += lasts[m] - ce[m]
                
                best_cost = find_best_sol_rec(ce, ne, quant, mill_clas, used, sol, act_pen + pen,best_cost, idx + 1, lasts) #falta fer act_pen + penalty
                for m in range(M):
                    if mill_clas[k][m]: lasts[m] -= 1
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
    sol = [-1]*C # place person with index 0 at the first position
    idx = 0 # next position to fill in sol
    act_pen = 0 # act_pen of sol (partial solution)
    used = [0]*K
    best_cost = C*C*M
    lasts = [0]*M
    cost = find_best_sol_rec(ce, ne, quant, mill_clas, used, sol, act_pen, best_cost, idx, lasts)
    print(time.time()- start)

    
main()