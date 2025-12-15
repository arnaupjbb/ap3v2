from yogi import *
import time
from sys import *
import random
import math
import heapq



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

def rangreedy2(
        C: int, M: int, K:int, ce: list[int], ne: list[int], 
        quant: list[int], mill_clas: list[list[bool]], pens:list[int], alfa
        ):
    
    """Donat un problema, generem una solució més o menys propera a un òptim amb un algorisme golafre.
    Per triar entre una classe i una altra prioritza: menor penalització que afegeix a la seqüència actual, 
    major quantitat de cotxes restants, major quantitat de suma de cotxes a afegir per les seves millores (val)
    i menor nombre de millores requerides, afegim component random on"""
    candlen = math.ceil(alfa*K)
    act_sol: list[int] = []
    act_pen: int = 0
    
    used: list[int] = [0]*K 
    rem: list[int] = [0]*M  # Guarda quants otxes queden per la millora m
    lasts: list[int] = [0]*M # Guarda quants cotxes amb la millora m tenim per l'última finestra de llargada ne[m]
    for m in range(M):
        for k in range(K):
            rem[m] += (quant[k]-used[k])*int(mill_clas[k][m])
    
    for i in range(C):
        candlist = []
        # Creem variables per guardar la millor penalizació fins al moment amb la seva classe, s
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
                
                heapq.heappush(candlist, (-pos_pen, -(used[k]-quant[k]), val, -pens[k], k))
                if len(candlist) > candlen:
                    heapq.heappop(candlist)
        # Actualitzem valors
        next_el = random.choice(candlist)
        next_k = next_el[-1]
        used[next_k] += 1
        for m in range(M):
            if mill_clas[next_k][m]:
                rem[m] -= 1
                lasts[m] += 1
            if i >= ne[m] and mill_clas[act_sol[-ne[m]]][m]:
                lasts[m] -= 1
        act_sol.append(next_k)
        act_pen += -next_el[0]

    # Afegim penalització final   
    for m in range(M):
        count = 0
        for i in range(C-1, max(C - ne[m], -1), -1):
            if mill_clas[act_sol[i]][m]:
                count += 1
            if count > ce[m]:
                act_pen += count - ce[m]

    return act_pen, act_sol

def calc_pen(solution: list[int], ce: list[int], ne: list[int], mill_clas: list[list[bool]]) -> int:
    """Donada una solució i les dades necessàries del problema (les capacitats de classes i les
    millores requerides) retorna la penalització de la solució"""
    C, M, K = len(solution), len(mill_clas[0]), len(mill_clas)
    lasts = [0]*M
    pen = 0
    for i in range(C):
        for m in range(M):
            if mill_clas[solution[i]][m]:
                lasts[m] += 1
            if i >= ne[m] and mill_clas[solution[i-ne[m]]][m]:
                lasts[m] -= 1
            pen += max(0, lasts[m] - ce[m])
    for m in range(M):
        count = 0
        for i in range(C-1, max(C - ne[m], -1), -1):
            if mill_clas[solution[i]][m]:
                count += 1
            if count > ce[m]:
                pen += count - ce[m]
    return pen

def metaheur(C, M, K, ce, ne, quant, mill_clas, pens, arch, start):

    # Paràmetres de randomització pel simulated annealing (TVAL, ALFAVAL), per quan triguem
    # en resetejar i per la randomització del greedy
    TVAL = 1. #temperatura de sim anneal
    ALFAVAL = 0.4   #alfa de sim anneal
    RESTART_CRIT = C*C//2   #criteri de fi de sim anneal
    ALFAGRASP = 0.1  #proporció que agafes de candidats
    random.seed(10)

    best_pen, best_sol = rangreedy2(C, M, K, ce, ne, quant, mill_clas, pens, ALFAGRASP)
    with open(arch,"w") as f: 
        endi = time.time()
        print(best_pen, round(endi - start,1), file=f)
        print(' '.join(map(str, best_sol)), file=f)
    iter = 0
    alfa = ALFAVAL
    T = TVAL
    real_best_sol, real_best_pen = best_sol, best_pen
    s= 0
    while s < 15000 and real_best_pen != 0:
        s += 1
        pos1 = random.randint(0, C-1)
        pos2 = random.randint(0, C-1)
        new_sol = best_sol.copy()
        new_sol[pos1], new_sol[pos2] = new_sol[pos2], new_sol[pos1]
        new_pen = calc_pen(new_sol, ce, ne, mill_clas)
        if iter > RESTART_CRIT:
            T = TVAL
            ALFAGRASP = (9*ALFAGRASP + 0.5)/10 
            new_pen, new_sol = rangreedy2(C, M, K, ce, ne, quant, mill_clas, pens, ALFAGRASP)
            iter = 0
        if new_pen <= best_pen or (random.uniform(0,1) < math.e**(-(new_pen - best_pen)/(T))):
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
