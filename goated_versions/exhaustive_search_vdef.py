from yogi import *
from sys import *
import time


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


def find_best_sol_rec(ce: list[int], ne: list[int], mill_clas: list[list[bool]], quant: list[int],
                      sol: list[int], used: list[int], lasts:list[int], remaining: list[int],
                      act_pen: int, best_cost: int, idx: int, addprox: int, start: float) -> int :
    """Resolem de manera recursiva el problema de trobar l'ordre per fabricar els cotxes amb menys
    penalitzacions. Donades capacitats (ce, ne), quines millores requereix cada classe (mill_clas),
    la quantitat de cotxes de cada classe a utilitzar (quant) i quant n'hem utilitzat (used),
    la solució parcial (sol), quants cotxes requereixen la millora m en la última finestra de tamany
    ne[m] (lasts) i els que queden per afegir de cada millora (remaining)."""
    C, M, K = len(sol), len(mill_clas[0]), len(used)
    if act_pen + addprox + lowbound(ce, ne, C-idx, remaining) >= best_cost : return best_cost

    if idx == C :
        # Si hem completat la solució, sumem la penalització de les últimes 
        # finestres i, si millorem, actualitzem
        for m in range(M):
            count = 0
            for i in range(C-1, max(C - ne[m], -1), -1):
                if mill_clas[sol[i]][m]:
                    count += 1
                if count > ce[m]:
                    act_pen += count - ce[m]
                if act_pen >= best_cost: return best_cost
                
        best_cost = act_pen
        with open(argv[1],"w") as f: 
            endi = time.time()
            print(best_cost, round(endi - start,1), file=f)
            print(' '.join(map(str, sol)), file=f)
        return best_cost
    
    else :
        for k in range(K):
            # Intentem afegir a la solució un cotxe de classe k
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
                
                best_cost = find_best_sol_rec(ce, ne, mill_clas, quant, sol, used, lasts, remaining, act_pen + pen,best_cost, idx + 1, addprox, start) 
                
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
    start = time.time()
    C, M, K, ce, ne, quant, mill_clas = read_prob()
    sol = [-1]*C
    used = [0]*K
    lasts = [0]*M
    remaining = [0]*M # quants cotxes queden per afegir que requereixin cada millora
    for m in range(M):
        for k in range(K):
            if mill_clas[k][m]:
                remaining[m] += quant[k]

    _ = find_best_sol_rec(ce, ne, mill_clas, quant, sol, used, lasts, remaining,0, C*C*M, 0, 0, start)
    
main()