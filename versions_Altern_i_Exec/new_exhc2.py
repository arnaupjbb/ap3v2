#!/usr/bin/env python3
from yogi import read
from sys import argv
import time
from typing import List

# ------------------ Lector ------------------
def read_prob():
    C, M, K = read(int), read(int), read(int)
    ce = [read(int) for _ in range(M)]
    ne = [read(int) for _ in range(M)]
    quant: List[int] = []
    mill_clas: List[List[int]] = [[] for _ in range(K)]
    for i in range(K):
        read(int)
        quant.append(read(int))
        for _ in range(M):
            mill_clas[i].append(1 if bool(read(int)) else 0)
    return C, M, K, ce, ne, quant, mill_clas

# ------------------ Solver ultra-rápido ------------------
def solve():
    C, M, K, ce, ne, quant, mill_clas = read_prob()

    seq: List[int] = [-1] * C
    remaining: List[int] = quant[:]

    best_cost: int = 10**9
    best_sol: List[int] = [-1] * C

    start = time.time()
    out_file = argv[1]

    # Ventanas deslizantes para cada opción
    window_count: List[int] = [0] * M
    window_queue: List[List[int]] = [ [0]*ne[j] for j in range(M) ]

    # ------------------ Escritura de la mejor solución ------------------
    def write_best(cost: int, sol: List[int]) -> None:
        end = time.time()
        with open(out_file, "w") as f:
            print(cost, round(end - start,1), file=f)
            print(" ".join(map(str, sol)), file=f)

    # ------------------ Backtracking puro con ventanas O(1) ------------------
    def backtrack(pos: int, curr_cost: int) -> None:
        nonlocal best_cost, best_sol
        if curr_cost >= best_cost:
            return
        if pos == C:
            best_cost = curr_cost
            for i in range(C):
                best_sol[i] = seq[i]
            write_best(best_cost, best_sol)
            return

        # Intentar cada clase con unidades restantes
        for cls in range(K):
            if remaining[cls] == 0:
                continue

            added = 0
            old_vals: List[int] = [0]*M  # para revertir
            # actualizar ventanas
            for j in range(M):
                old = window_queue[j][pos % ne[j]]
                old_vals[j] = old
                subtract = old
                window_count[j] -= subtract
                add = mill_clas[cls][j]
                window_queue[j][pos % ne[j]] = add
                window_count[j] += add
                if window_count[j] > ce[j]:
                    added += window_count[j] - ce[j]

            if curr_cost + added >= best_cost:
                # revertir
                for j in range(M):
                    window_count[j] -= window_queue[j][pos % ne[j]]
                    window_queue[j][pos % ne[j]] = old_vals[j]
                    window_count[j] += old_vals[j]
                continue

            # aplicar
            seq[pos] = cls
            remaining[cls] -= 1

            backtrack(pos + 1, curr_cost + added)

            # deshacer
            seq[pos] = -1
            remaining[cls] += 1
            for j in range(M):
                window_count[j] -= window_queue[j][pos % ne[j]]
                window_queue[j][pos % ne[j]] = old_vals[j]
                window_count[j] += old_vals[j]

    backtrack(0, 0)

    if best_sol[0] == -1:
        with open(out_file, "w") as f:
            print("No solution", file=f)

if __name__ == "__main__":
    solve()
