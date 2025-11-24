from yogi import *
from time import time
import sys


def nou_cost(
    sol: list[int], millores: list[list[int]], idx: int, ce: list[int], ne: list[int]
)-> int:
    """Retorna la suma dels costos de cada estació per a l'interval [max(idx-ne[i], 0), idx] per cada i. 
    També retorna una cota inferior de la penalització futura a partir de la solució fins a idx."""
    M = len(ce)
    C = len(sol)
    cost = 0
    for i in range(M):
        ocupacio_estacio = 0
        for j in range(idx, max(-1, idx - ne[i]), -1):
            ocupacio_estacio += millores[sol[j]][i]
            cost += max(0, ocupacio_estacio - ce[i])
    return cost


def min_pen(
    C: int,
    cotxes_classe: list[int],
    millores: list[list[int]],
    ce: list[int],
    ne: list[int],
    inici: float,
) -> int:
    """Retorna el mínim cost de fabricació donats una matriu de millores, un vector de 
    capacitats ce, un vector de finestres ne i els cotxes a fabricar de cada classe cotxes_classe"""
    sol = [-1] * C
    classes_restants = cotxes_classe.copy()
    total_cost = 0
    K = len(cotxes_classe)
    M = len(ce)
    for i in range(C):
        best_cost = sys.maxsize
        best_class = 0
        for j in range(K):
            if classes_restants[j] > 0:
                sol[i] = j
                cost = nou_cost(sol, millores, i, ce, ne)
                if cost < best_cost:
                    best_cost = cost
                    best_class = j
                if cost == best_cost:
                    if classes_restants[best_class] < classes_restants[j]:
                        best_class = j
        classes_restants[best_class] -= 1
        sol[i] = best_class
        total_cost += best_cost
    for i in range(M):
        ocupacio_estacio = 0
        for j in range(max(C - ne[i], 0), C - 1):
            ocupacio_estacio += millores[sol[j]][i]
            best_cost += max(0, ocupacio_estacio - ce[i])
    try:
        with open(sys.argv[1], "w") as f:
            final = time()
            print(total_cost, round(final - inici, 1), file=f)
            print(" ".join(map(str, sol)), file=f)
    except IndexError:
        print("Error. No s'ha rebut cap fitxer de sortida")
        return -1
    return total_cost




def read_input() -> tuple[int, list[int], list[list[int]], list[int], list[int]]:
    """Llegeix l'entrada del problema i retorna:
    C: nombre total de cotxes,
    cotxes_classe: nombre de cotxes a fabricar de cada classe,
    millores: matriu on cada fila correspon a una classe, i cada element m_ij indica si
    el cotxe de la classe i necessita la millora j,
    ce: vector de capacitats,
    ne: vector de finestres."""
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
