from yogi import *
from time import time
import sys

def nou_cost(sol: list[int], millores:list[list[int]], idx: int, ce: list[int], ne:list[int]) -> int:
    M = len(ce)
    C = len(sol)
    nou_cost = 0
    for i in range(M):
        ocupacio_estacio = 0
        for j in range(idx, max(-1, idx-ne[i]), -1):
            ocupacio_estacio += millores[sol[j]][i]
        nou_cost += max(0, ocupacio_estacio - ce[i])
    return nou_cost

def min_pen_rec(sol: list[int], classes_restants: list[int], millores: list[list[int]], cost_actual: int, idx: int, ce: list[int], ne: list[int], min_cost: list[int], inici: float):
    C = len(sol)
    M = len(millores[0])
    K = len(millores)
    if cost_actual >= min_cost[0]:
        return cost_actual, sol
    if idx == C:
        for i in range(M):
            ocupacio_estacio = 0
            for j in range(idx-1, max(-1, idx-ne[i]), -1):
                ocupacio_estacio += millores[sol[j]][i]
                cost_actual += max(0, ocupacio_estacio - ce[i])
        if cost_actual < min_cost[0]:
            min_cost[0] = cost_actual
            try:
                with open(sys.argv[1],"w") as f: 
                    final = time()
                    print(cost_actual, round(final - inici,1), file=f)
                    print(' '.join(map(str, sol)), file=f)
            except IndexError:
                print("Error. No s'ha rebut cap fitxer de sortida")
                min_cost[0] = -1
                return -1, sol
        return cost_actual, sol.copy()
    else:
        best_cost = sys.maxsize
        best_sol = [-1]*C
        for i in range(K):
            if classes_restants[i] != 0:
                nou_cotxe = i
                classes_restants[i] -= 1
                sol[idx] = nou_cotxe
                nc = nou_cost(sol, millores, idx, ce, ne)
                cost, new_sol = min_pen_rec(sol, classes_restants, millores, cost_actual+nc, idx+1, ce, ne, min_cost, inici)
                if cost < best_cost:
                    best_cost = cost
                    best_sol = new_sol
                sol[idx] = -1
                classes_restants[i] += 1 
        return best_cost, best_sol
    
def min_pen(C: int, cotxes_classe: list[int], millores: list[list[int]], ce: list[int], ne: list[int], inici: float):
    sol = [-1]*C
    classes_restants = cotxes_classe.copy()
    cost_actual = 0
    idx = 0
    min_cost = [sys.maxsize]
    best_cost, best_sol = min_pen_rec(sol, classes_restants, millores, cost_actual, idx, ce, ne, min_cost, inici)
    return best_cost, best_sol


def read_input() -> tuple[int, list[int], list[list[int]], list[int], list[int]]:
    C = read(int)
    M = read(int)
    K = read(int)
    ce = [read(int) for _ in range(M)]
    ne = [read(int) for _ in range(M)]
    cotxes_classe = [-1]*K
    millores = [[-1]*M for _ in range(K)]
    for _ in range(K):
        i = read(int)
        cotxes_classe[i] = read(int)
        millores[i] = [read(int) for _ in range (M)]
    return C, cotxes_classe, millores, ce, ne

def main():
    C, cotxes_classe, millores, ce, ne = read_input()
    inici = time()
    cost, sol= min_pen(C, cotxes_classe, millores, ce, ne, inici)
    final = time()
    print(cost, round(final - inici,1))
    print(' '.join(map(str, sol)))

main()

    