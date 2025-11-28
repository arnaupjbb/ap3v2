from yogi import *
import time
from sys import *
import random
import math


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
        quant: list[int], mill_clas: list[list[bool]], pens:list[int], undecadax
        ):
    
    """Donat un problema, generem una solució més o menys propera a un òptim amb un algorisme golafre.
    Per triar entre una classe i una altra prioritza: menor penalització que afegeix a la seqüència actual, 
    major quantitat de cotxes restants, major quantitat de suma de cotxes a afegir per les seves millores (val)
    i menor nombre de millores requerides, afegim component random on"""
    act_sol: list[int] = []
    act_pen: int = 0
    used: list[int] = [0]*K 
    rem: list[int] = [0]*M  # Guarda quants otxes queden per la millora m
    lasts: list[int] = [0]*M # Guarda quants cotxes amb la millora m tenim per l'última finestra de llargada ne[m]
    for m in range(M):
        for k in range(K):
            rem[m] += (quant[k]-used[k])*int(mill_clas[k][m])
    
    for i in range(C):
        breakpoint = random.randint(1, K*undecadax) if undecadax != 0 else -1
        # Si surt un nombre entre 1 i K intentarem agafar aquesta classe, sinó ho ignorarem

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
                
                if k == breakpoint or ((pos_pen, used[k]-quant[k], -val, pens[k]) < 
                        (next_pen, used[next_k]-quant[next_k], -next_val, pens[next_k])):
                    # Triem entre la classe a explorar i la millor trobada i actualitzem
                    next_pen = pos_pen
                    next_k  = k
                    next_val = val
                if k == breakpoint:
                    # Si la k és la que hem decidit amb randint, parem de buscar i l'afegim a la llista
                    break
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
    TVAL = 1.
    ALFAVAL = 0.1
    RESTART_CRIT = 500
    RANDOMPROB = K//4 + 1
    best_pen, best_sol = rangreedy2(C, M, K, ce, ne, quant, mill_clas, pens, 0)
    with open(arch,"w") as f: 
        endi = time.time()
        print(best_pen, round(endi - start,1), file=f)
        print(' '.join(map(str, best_sol)), file=f)
    iter = 0
    alfa = ALFAVAL
    T = TVAL
    real_best_sol, real_best_pen = best_sol, best_pen
    while True:
        pos1 = random.randint(0, C-1)
        pos2 = random.randint(0, C-1)
        new_sol = best_sol.copy()
        new_sol[pos1], new_sol[pos2] = new_sol[pos2], new_sol[pos1]
        new_pen = calc_pen(new_sol, ce, ne, mill_clas)
        if iter > RESTART_CRIT:
            # Calulate randomized greedy again sense això és sim anneal
            T = TVAL
            new_pen, new_sol = rangreedy2(C, M, K, ce, ne, quant, mill_clas, pens, RANDOMPROB)
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
