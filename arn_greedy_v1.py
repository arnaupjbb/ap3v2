from yogi import *
import time
from sys import *


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


def greedy(
        C: int, M: int, K:int, ce: list[int], ne: list[int], 
        quant: list[int], mill_clas: list[list[bool]]
        ):
    
    """Given a problem, generates a good solution using a greedy algorithm"""
    act_sol = []
    act_pen = 0
    used = [0]*K
    for i in range(C):
        next_pen = C*C*M
        next_k = -1
        for k in range(K):
            if used[k] < quant[k] :
                pos_pen = add_pen(M, i+1, ne, mill_clas, act_sol + [k], ce)
                if pos_pen < next_pen:
                    next_pen = pos_pen
                    next_k  = k
                # if pos_pen == 0: break
        used[next_k] += 1
        act_sol.append(next_k)
        act_pen += next_pen
    for m in range(M):
        count = 0
        for i in range(C-1, max(C - ne[m], -1), -1):
            if mill_clas[act_sol[i]][m]:
                count += 1
            if count > ce[m]:
                act_pen += count - ce[m]
    return act_pen, act_sol
            

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
    best_pen, best_sol = greedy(
        C, M, K, ce, ne, quant, mill_clas, [0]*K
        )
    with open(arch,"w") as f: 
        endi = time.time()
        print(best_pen, round(endi - start,1), file=f)
        print(' '.join(map(str, best_sol)), file=f)
   
main()
