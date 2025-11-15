from yogi import *
import time
from sys import *


### MILLOR VERSIÓ TROBADA FINS EL MOMENT

def add_pen(M, L, ne, mill_clas, act_sol, ce) -> int:
    """ Given some information of the problem (M, L, ne, mill_clas, ce) and the partial solution, 
    it returns the penalty caused by the last addition . It can be used for the starting
    intervals too (even if they are shorter than the ne), but does not return the penalty 
    to add for the last shorter intervals"""

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
        best_sol: list[int], start, arch
        ):
    
    """It returns the solution with less penalty given a problem and a partial solution
    and modifies the list best_sol giving the solution with the best solution found, it writes
    the best solution found in the given output file when found, next to its penalty and time spent 
    to found it"""
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
                if act_pen >= best_pen: return best_pen
                
                

        best_sol = act_sol
        with open(arch,"w") as f: 
            endi = time.time()
            print(act_pen, round(endi - start,1), file=f)
            print(' '.join(map(str, best_sol)), file=f)
        return act_pen
    
    for k in range(K):
        if used[k] < quant[k]:
            act_sol.append(k)
            used[k] += 1

            new_p = add_pen(M, L + 1, ne, mill_clas, act_sol, ce)
            best_pen = exh_sch(
                C, M, K, ce, ne, quant, mill_clas,
                act_pen + new_p, act_sol, used,
                best_pen, best_sol, start, arch
                )


            used[k] -= 1
            act_sol.pop()
    return best_pen     

def read_prob() -> tuple[int, int, int, list[int], list[int], list[int], list[list[bool]]]:
    """Reads the problem and returns its data"""
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
    _ = exh_sch(
        C, M, K, ce, ne, quant, mill_clas,
        0, [],[0]*K, C*C*M, [0]*C, start, arch
        )
    print(round(time.time() - start))
   
main()
