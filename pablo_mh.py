from yogi import *
from time import time
import sys
import random

E = 2.718281828459 
INITIAL_T = 1.0
BETA = 0.99

def nou_cost(
    sol: list[int], millores: list[list[int]], idx: int, ce: list[int], ne: list[int]
)-> tuple[int, int]:
    """Retorna la suma dels costos de cada estació per a l'interval [max(idx-ne[i], 0), idx] per cada i. 
    També retorna una cota inferior de la penalització futura a partir de la solució fins a idx."""
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

def sol_cost(sol: list[int], millores: list[list[int]], ce:list[int], ne:list[int]):
    M = len(ce)
    C = len(sol)
    cost = 0
    for m in range(M):
        ocupacio_estacio = 0
        window_length = ne[m]
        for i in range(C+window_length-1):
            if i < C:
                ocupacio_estacio += millores[sol[i]][m]
            window_idx = i - window_length + 1
            if window_idx > 0:
                ocupacio_estacio -= millores[sol[window_idx-1]][m]
            cost += max(ocupacio_estacio - ce[m], 0)
    return cost


def build_solution(
    C: int,
    cotxes_classe: list[int],
    millores: list[list[int]],
    ce: list[int],
    ne: list[int],
    alpha: float
    ) -> list[int]:
    """Retorna el mínim cost de fabricació donats una matriu de millores, un vector de 
    capacitats ce, un vector de finestres ne i els cotxes a fabricar de cada classe cotxes_classe"""
    sol = [-1] * C
    classes_restants = cotxes_classe.copy()
    K = len(cotxes_classe)
    min_cost = sys.maxsize
    for i in range(C):
        class_scores = []
        classes = [i for i in range(K)]
        random.shuffle(classes)
        for k in classes:
            if classes_restants[k] != 0:
                sol[i] = k
                cost, aprox = nou_cost(sol, millores, i, ce, ne)
                class_scores.append((cost+aprox, classes_restants[k], k))
        L = int(max(alpha*len(class_scores), 1))
        class_scores = sorted(class_scores, key=lambda x: (x[0], -x[1]))[:L]
        candidate = class_scores[random.randint(0, L-1)][2]
        sol[i] = candidate
        classes_restants[candidate] -= 1
    return sol

def grasp(C: int, cotxes_classe: list[int], millores: list[list[int]], ce: list[int], ne: list[int], min_cost:int, inici:float, alpha: float) -> int:
    sol = build_solution(C, cotxes_classe, millores, ce, ne, alpha)
    T = INITIAL_T
    k = 0
    cost = sol_cost(sol, millores, ce, ne)
    while k < 500:
        n1 = random.randint(0, C-1)
        n2 = random.randint(0, C-1)
        while n1 == n2:
            n2 = random.randint(0, C-1)
        neighbour_sol = sol.copy()
        neighbour_sol[n1], neighbour_sol[n2] = neighbour_sol[n2], neighbour_sol[n1]
        n_cost = sol_cost(neighbour_sol, millores, ce, ne)
        if n_cost < cost:
            sol = neighbour_sol
            cost = n_cost
            if cost < min_cost:
                min_cost = cost
                with open(sys.argv[1], "w") as f:
                    final = time()
                    print(min_cost, round(final - inici, 1), file=f)
                    print(" ".join(map(str, sol)), file=f)
        else:
            prob = E**(-(n_cost-cost)/T)
            R = random.random()
            if R < prob: 
                sol = neighbour_sol
                cost = n_cost  
        T = BETA * T
        k += 1
    return min_cost




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
    min_cost = sys.maxsize
    C, cotxes_classe, millores, ce, ne = read_input()
    inici = time()
    k = 0
    alpha = 0.3
    while True:
        new_min_cost = grasp(C, cotxes_classe, millores, ce, ne, min_cost, inici, alpha)
        k += 1
        if new_min_cost != min_cost:
            k = 0
            min_cost = new_min_cost
        if k >= 1000:
            if alpha < 0.98:
                alpha += 0.02

main()
