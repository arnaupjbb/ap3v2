from yogi import *
from time import time
import sys


def nou_cost(
    sol: list[int], millores: list[list[int]], idx: int, ce: list[int], ne: list[int]
) -> tuple[int, int]:
    M = len(ce)
    C = len(sol)
    nou_cost = 0
    aprox = 0
    for i in range(M):
        ocupacio_estacio = 0
        for j in range(idx, max(-1, idx - ne[i]), -1):
            ocupacio_estacio += millores[sol[j]][i]
        n = max(0, ocupacio_estacio - ce[i])
        nou_cost += n
        aprox += n*(n-1)//2 
    return nou_cost, aprox


def min_pen_rec(
    sol: list[int],
    classes_restants: list[int],
    millores: list[list[int]],
    cost_actual: int,
    idx: int,
    ce: list[int],
    ne: list[int],
    min_cost: int,
    inici: float,
    aprox: int
) -> int:
    C = len(sol)
    M = len(millores[0])
    K = len(millores)
    if cost_actual + aprox >= min_cost:
        return min_cost
    if idx == C:
        for i in range(M):
            ocupacio_estacio = 0
            for j in range(idx - 1, max(-1, idx - ne[i]), -1):
                ocupacio_estacio += millores[sol[j]][i]
                cost_actual += max(0, ocupacio_estacio - ce[i])
        if cost_actual < min_cost:
            min_cost = cost_actual
            try:
                with open(sys.argv[1], "w") as f:
                    final = time()
                    print(cost_actual, round(final - inici, 1), file=f)
                    print(" ".join(map(str, sol)), file=f)
            except IndexError:
                print("Error. No s'ha rebut cap fitxer de sortida")
                min_cost = -1
                return -1
        return min_cost
    else:
        for i in range(K):
            if classes_restants[i] != 0:
                nou_cotxe = i
                classes_restants[i] -= 1
                sol[idx] = nou_cotxe
                nc, aprox = nou_cost(sol, millores, idx, ce, ne)
                min_cost = min_pen_rec(
                    sol,
                    classes_restants,
                    millores,
                    cost_actual + nc,
                    idx + 1,
                    ce,
                    ne,
                    min_cost,
                    inici,
                    aprox
                )
                classes_restants[i] += 1
        return min_cost


def min_pen(
    C: int,
    cotxes_classe: list[int],
    millores: list[list[int]],
    ce: list[int],
    ne: list[int],
    inici: float,
) -> int:
    sol = [-1] * C
    classes_restants = cotxes_classe.copy()
    cost_actual = 0
    idx = 0
    min_cost = sys.maxsize
    aprox = 0
    best_cost = min_pen_rec(
        sol, classes_restants, millores, cost_actual, idx, ce, ne, min_cost, inici, aprox
    )
    return best_cost


def read_input() -> tuple[int, list[int], list[list[int]], list[int], list[int]]:
    C = read(int)
    M = read(int)
    K = read(int)
    ce = [read(int) for _ in range(M)]
    ne = [read(int) for _ in range(M)]
    cotxes_classe = [-1] * K
    millores = [[-1] * M for _ in range(K)]
    for _ in range(K):
        i = read(int)
        cotxes_classe[i] = read(int)
        millores[i] = [read(int) for _ in range(M)]
    return C, cotxes_classe, millores, ce, ne


def main():
    C, cotxes_classe, millores, ce, ne = read_input()
    inici = time()
    cost = min_pen(C, cotxes_classe, millores, ce, ne, inici)
    final = time()
    print(round(final - inici, 1), cost)


main()
