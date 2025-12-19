from yogi import *
import time
from sys import *
import random
import math
import heapq


def lowbound(ce: list[int], ne: list[int], c2add: int, remaining: list[int]) -> int:
    """ Calculem una fita inferior per la penalització que queda per afegir donats
    les llistes de capacitats (ce, ne), el cotxes que queden a afegir en total i els
    cotxes que queden a afegir per cada millora"""
    min_pen = 0
    M = len(ne)
    for m in range(M):
       if c2add > ce[m]:
           # Afegim un mínim de penalització contant cada un de les ne[m] + c2add - 1 finestres 
           # per separat. Calculem els "cotxes totals a afegir" comptant que cadascun està a ne[m]
           # finestres i li restem la capacitat total sense penalitzacions.
           min_pen += max(0, remaining[m] * ne[m] - ce[m] * (c2add + ne[m] - ce[m]))
    return min_pen


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
        ) -> tuple[int, list[int]]:
    
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
        next_el = random.choice(candlist) #triem una classe random entre la llista de candidats
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


def calc_pen2(solution: list[int], ce: list[int], ne: list[int], 
              mill_clas: list[list[bool]], last_pen: int, pos1: int, pos2: int) -> int:
    """Donada una solució amb 2 posicions canviades, dades del problema, i les posicions canviades, 
    calcula penalització de la nova solució"""
    C, M = len(solution), len(mill_clas[0])
    if pos1 == pos2: return last_pen
    for m in range(M):
        if mill_clas[solution[pos1]][m] != mill_clas[solution[pos2]][m]:
            new_imp = pos1 if mill_clas[solution[pos1]][m] else pos2
            no_imp = pos1+pos2-new_imp

            # Calculem primer el canvi per la posició que passa de no tenir millora a tenir-la
            count = 0
            for i in range(max(0,new_imp -ne[m]), new_imp):
                count += int(mill_clas[solution[i]][m])
            
            for end in range(new_imp, new_imp + ne[m]):
                if end - ne[m] >= 0 and mill_clas[solution[end - ne[m]]][m]:
                    count -= 1
                if end < C and mill_clas[solution[end]][m]:
                    count += 1
                if end - ne[m] + 1 <= no_imp <= end: continue
                if count > ce[m]: last_pen += 1  
            count = 0
            for i in range(max(0,no_imp -ne[m]), no_imp):
                count += int(mill_clas[solution[i]][m])
            
            for end in range(no_imp, no_imp + ne[m]):
                
                if end - ne[m] >= 0 and mill_clas[solution[end - ne[m]]][m]:
                    count -= 1
                if end < C and mill_clas[solution[end]][m]:
                    count += 1
                if end - ne[m] + 1 <= new_imp <= end: continue
                if count >= ce[m]: last_pen -= 1    
    return last_pen


def metaheur(C: int, M: int, K: int, ce: list[int], ne: list[int], quant: list[int], 
            mill_clas: list[list[bool]], pens: list[int], start: float) -> None:
    """Resolem el problema dels cotxes amb una heurística GRASP utilitzant simulated annealing"""

    # Paràmetres de randomització pel simulated annealing (TVAL, ALFAVAL), per quan triguem
    # en resetejar (Restart_crit), per la randomització del greedy (alfagrasp) i la seed.
    TVAL = 1. # Temperatura de sim anneal
    ALFAVAL = 0.999  # Alfa de sim anneal
    RESTART_CRIT = C*C  #criteri de fi de sim anneal (iteracions sense millorar ni estar 
                        #igual que la millor solució trobada)
    ALFAGRASP = 0.1  #proporció que agafes de candidats al greedy
    EQLIM = C*C*5  # Límit per iteracions on la solució te penalització
    MAXALFAGRASP = 0.4 # Alfa a la que convergirem
    SEED = 122
    random.seed(SEED)

    remaining = [0]*M
    for m in range(M):
        for k in range(K):
            if mill_clas[k][m]:
                remaining[m] += quant[k]
    MINIMUM_POSSIBLE_PEN = lowbound(ce, ne, C, remaining)

    best_pen, best_sol = rangreedy2(C, M, K, ce, ne, quant, mill_clas, pens, ALFAGRASP)
    with open(argv[1],"w") as f: 
        endi = time.time()
        print(best_pen, round(endi - start,1), file=f)
        print(' '.join(map(str, best_sol)), file=f)
    iter = 0
    alfa = ALFAVAL
    T = TVAL
    real_best_sol, real_best_pen = best_sol, best_pen
    last_pen = best_pen
    eqcas = 0
    while real_best_pen > MINIMUM_POSSIBLE_PEN:
        new_pen = -1
        if iter > RESTART_CRIT or eqcas > EQLIM:
            RESTART_CRIT = min(C*C*C, RESTART_CRIT + C*C//10)
            T = TVAL
            ALFAGRASP = (9*ALFAGRASP + MAXALFAGRASP)/10
            best_pen, best_sol = rangreedy2(C, M, K, ce, ne, quant, mill_clas, pens, ALFAGRASP)
            iter = 0
            eqcas = 0
            if best_pen < real_best_pen:
                real_best_pen = best_pen
                real_best_sol = best_sol[:]
                with open(argv[1],"w") as f: 
                    endi = time.time()
                    print(real_best_pen, round(endi - start,1), file=f)
                    print(' '.join(map(str, real_best_sol)), file=f)
        else:    
            pos1 = random.randint(0, C-1)
            pos2 = random.randint(0, C-1)
            if pos1 == pos2: continue
            best_sol[pos1], best_sol[pos2] = best_sol[pos2], best_sol[pos1]
            new_pen = calc_pen2(best_sol, ce, ne, mill_clas, last_pen, pos1, pos2)
        
            if new_pen <= best_pen or (random.uniform(0,1) < math.e**(-(new_pen - best_pen)/(T))):
                best_pen = new_pen
                if best_pen == real_best_pen:
                    iter = 0
                    eqcas += 1
                if best_pen < real_best_pen:
                    real_best_pen = new_pen
                    real_best_sol = best_sol[:]
                    iter = 0
                    eqcas = 0
                    
                    with open(argv[1],"w") as f: 
                        endi = time.time()
                        print(real_best_pen, round(endi - start,1), file=f)
                        print(' '.join(map(str, real_best_sol)), file=f)
            else:
                # Si no hem quedat amb al nova solució, tornem a la posició anterior
                best_sol[pos1], best_sol[pos2] = best_sol[pos2], best_sol[pos1]
            
        # Preparem següent iteració
        last_pen = best_pen
        iter += 1
        T *= alfa

        
def main():
    start = time.time()
    C, M, K, ce, ne, quant, mill_clas, pens = read_prob()
    metaheur(C, M, K, ce, ne, quant, mill_clas, pens, start)

main()
