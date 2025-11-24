from yogi import *
import time
from sys import *
import random

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
    if pos_pen + addprox != next_pen + next_addprox:
        return pos_pen + addprox < next_pen + next_addprox
    if prop_next != used[k] -quant[k]:
        return prop_next > used[k] -quant[k]
    if val[k] != val[next_k]:
        return val[k] > val[next_k]
    return pens[k] > pens[next_k]

def rangreedy(
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
        prop_next =  -1
        for k in range(K):
            if used[k] < quant[k] :
                pos_pen, addprox = add_pen(M, i+1, ne, mill_clas, act_sol + [k], ce)
                for m in range(M):
                    if mill_clas[k][m]:
                        val[k] += rem[m]
                if is_better22(k, pos_pen, next_k, next_pen, prop_next, pens, quant, used, addprox, next_pen_add, val) or random.randint(1, 50) == 1:
                    next_pen = pos_pen
                    next_pen_add = addprox
                    next_k  = k
                    prop_next = used[k] - quant[k]
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


def calc_pen(solution, ce, ne, mill_clas):
    C, M, K = len(solution), len(mill_clas[0]), len(mill_clas)
    pen = 0
    for i in range(C):
        np, _ = add_pen(M, i+1, ne, mill_clas, solution[:i+1], ce)
        pen += np
    for m in range(M):
        count = 0
        for i in range(C-1, max(C - ne[m], -1), -1):
            if mill_clas[solution[i]][m]:
                count += 1
            if count > ce[m]:
                pen += count - ce[m]
    return pen

def metaheur(C, M, K, ce, ne, quant, mill_clas, pens, arch, start):
    best_pen, best_sol = rangreedy(C, M, K, ce, ne, quant, mill_clas, pens)
    with open(arch,"w") as f: 
        endi = time.time()
        print("greedy", best_pen, round(endi - start,1), file=f)
        print(' '.join(map(str, best_sol)), file=f)
    iter = 0
    alfa = 0.01
    T = 10.
    real_best_sol, real_best_pen = best_sol, best_pen
    while True:
        pos1 = random.randint(0, C-1)
        pos2 = random.randint(0, C-1)
        new_sol = best_sol.copy()
        new_sol[pos1], new_sol[pos2] = new_sol[pos2], new_sol[pos1]
        new_pen = calc_pen(new_sol, ce, ne, mill_clas)
        if iter > 10000:
            T = 10.
            new_pen, new_sol = rangreedy(C, M, K, ce, ne, quant, mill_clas, pens)
            iter = 0
        if new_pen < best_pen or (random.uniform(0,1) < 2.71828**(-(new_pen - best_pen)/(T))):
            best_sol = new_sol[:]
            best_pen = new_pen
            if new_pen < real_best_pen:
                real_best_pen = new_pen
                real_best_sol = new_sol[:]
                iter = 0
                with open(arch,"w") as f: 
                    endi = time.time()
                    print(real_best_pen, round(endi - start,1), file=f)
                    print(' '.join(map(str, real_best_sol)), file=f)
        iter += 1
        T *= alfa
def main():
    start = time.time()
    C, M, K, ce, ne, quant, mill_clas, pens = read_prob()
    arch = argv[1]
    metaheur(C, M, K, ce, ne, quant, mill_clas, pens, arch, start)
    
main()
