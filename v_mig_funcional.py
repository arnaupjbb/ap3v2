from yogi import *
import time
from sys import *

### VERSIO AMB LASTS, MÉS LENTA
def add_pen(M, L, ne, mill_clas, act_sol, ce) -> int:
    new_p = 0
    for m in range(M):
        count = 0
        for i in range(max(L - ne[m], 0), L):
            if mill_clas[act_sol[i]][m]:
                count += 1
        if count > ce[m]:
            new_p += count - ce[m]
    return new_p

def exh_sch(
        C: int, M: int, K:int, ce: list[int], ne: list[int], 
        quant: list[int], mill_clas: list[list[bool]],act_pen: int,
        act_sol:list[int], used: list[int], best_pen: int, 
        best_sol: list[int], start, arch, lasts
        ):
    if act_pen >= best_pen:
        return best_pen
    L: int = len(act_sol)

    if L == C:
        for m in range(M):
            count = 0
            for i in range(L-1, max(L - ne[m], -1), -1):
                if mill_clas[act_sol[i]][m]:
                    count += 1
                if count > ce[m]:
                    act_pen += count - ce[m]
                
                
        if act_pen < best_pen:
            best_pen = act_pen
            best_sol = act_sol
            with open(arch,"w") as f: 
                endi = time.time()
                print(best_pen, round(endi - start,1), file=f)
                print(' '.join(map(str, best_sol)), file=f)
        return best_pen
    
    for k in range(K):
        if used[k] < quant[k]:
            act_sol.append(k)
            used[k] += 1
            L += 1
            new_p = 0
            for m in range(M):
                if mill_clas[k][m]:
                    lasts[m] += 1
                if L > ne[m] and mill_clas[act_sol[-ne[m] - 1]][m]:
                    lasts[m] -= 1
                if lasts[m] > ce[m]:
                    new_p += lasts[m] - ce[m]
            best_pen = exh_sch(
                C, M, K, ce, ne, quant, mill_clas,
                act_pen + new_p, act_sol, used,
                best_pen, best_sol, start, arch, lasts
                )

            for m in range(M):
                if mill_clas[k][m]:
                    lasts[m] -= 1
                if L > ne[m] and mill_clas[act_sol[-ne[m] - 1]][m]:
                    lasts[m] += 1
            L -= 1
            used[k] -= 1
            act_sol.pop()
    return best_pen     

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
        for j in range(M):
            mill_clas[i].append(bool(read(int)))
    return C, M, K, ce, ne, quant, mill_clas


def main():
    start = time.time() 
    C, M, K, ce, ne, quant, mill_clas = read_prob()
    arch = argv[1]
    lasts = [0]*M
    _ = exh_sch(
        C, M, K, ce, ne, quant, mill_clas,
        0, [],[0]*K, C*C*M, [0]*C, start, arch, lasts
        )
    print(round(time.time() - start))
   
main()
