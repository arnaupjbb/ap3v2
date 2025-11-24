from yogi import *
import time
from sys import *

#VERSIO ON MIREM menys pen_add -> mes suma remain -> mes penalitzacions de clase -> menys percentatge d'us
def add_pen(M, L, ne, mill_clas, act_sol, ce) -> tuple[int, int]:
    """ Given some information of the problem (M, L, ne, mill_clas, ce) and the partial solution, 
    it returns the penalty caused by the last addition . It can be used for the starting
    intervals too (even if they are shorter than the ne), but does not return the penalty 
    to add for the last shorter intervals"""

    new_p = 0
    addprox = 0
    for m in range(M):
        count = 0
        for i in range(max(L - ne[m], 0), L):
            if mill_clas[act_sol[i]][m]:
                count += 1
        if count > ce[m]:
            new_p += count - ce[m]
            addprox += (count - ce[m])*(count - ce[m] - 1)//2
    return new_p, addprox

def usrate(M, K, rem, used, quants, mill_clas):
    remain_rate = [0.]*M
    if rem == 0:
        return remain_rate
    for m in range(M):
        for k in range(K):
            remain_rate[m] += float((quants[k]-used[k])*int(mill_clas[k][m]))
        remain_rate[m] /= rem
    return remain_rate

def is_better22(k, pos_pen, next_k, next_pen, prop_next, pens, quant, used, addprox, next_addprox, val) -> bool:
    if pos_pen < next_pen:
        return True
    if pos_pen > next_pen:
        return False
    if val[k] > val[next_k]:
        return True
    if val[k] < val[next_k]:
        return False
    if pens[k] > pens[next_k]:
        return True
    if pens[k] < pens[next_k]:
        return False
    return prop_next > used[k]/quant[k]

def greedy(
        C: int, M: int, K:int, ce: list[int], ne: list[int], 
        quant: list[int], mill_clas: list[list[bool]], pens:list[int]
        ):
    
    """Given a problem, generates a good solution using a greedy algorithm"""
    act_sol = []
    act_pen = 0
    used = [0]*K
    for i in range(C):
        next_pen = C*C*M
        next_pen_add = C*C*M
        rem = usrate(M, K, C-i, used, quant, mill_clas)
        val = [-1.]*K
        next_k = 0
        prop_next =  1.1
        for k in range(K):
            if used[k] < quant[k] :
                pos_pen, addprox = add_pen(M, i+1, ne, mill_clas, act_sol + [k], ce)
                for m in range(M):
                    if mill_clas[k][m]:
                        val[k] += rem[m]
                if is_better22(k, pos_pen, next_k, next_pen, prop_next, pens, quant, used, addprox, next_pen_add, val):
                    next_pen = pos_pen
                    next_pen_add = addprox
                    next_k  = k
                    prop_next = used[k]/quant[k]
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
        for j in range(M):
            have = bool(read(int))
            mill_clas[i].append(have)
            if have:
                pens[i] += 1
    return C, M, K, ce, ne, quant, mill_clas, pens



def main():
    start = time.time()
    C, M, K, ce, ne, quant, mill_clas, pens = read_prob()
    arch = argv[1]
    best_pen, best_sol = greedy(
        C, M, K, ce, ne, quant, mill_clas, pens
        )
    with open(arch,"a") as f: 
        endi = time.time()
        print(best_pen, round(endi - start,1), file=f)
        print(' '.join(map(str, best_sol)), file=f)
   
main()
