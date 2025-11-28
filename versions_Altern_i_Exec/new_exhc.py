from yogi import read
from sys import argv
import time

def read_prob():
    C = read(int)
    M = read(int)
    K = read(int)

    ce = [read(int) for _ in range(M)]
    ne = [read(int) for _ in range(M)]

    quant = [0] * K
    mill_clas = [[0]*M for _ in range(K)]
    for i in range(K):
        _ = read(int)
        quant[i] = read(int)
        for j in range(M):
            mill_clas[i][j] = 1 if read(int) else 0

    return C, M, K, ce, ne, quant, mill_clas

def solve():
    C, M, K, ce, ne, quant, mill_clas = read_prob()

    seq = [-1] * C
    remaining = quant[:]     # coches por clase

    # Ventanas deslizantes
    win_count = [0] * M
    win_queue = [ [0]*ne[j] for j in range(M) ]

    # sumas dentro del bloque en curso (parciales)
    current_block = [0]*M

    # para cada opción j: espacio para almacenar las sumas de bloques completos
    # max_blocks por opción (una cota razonable)
    max_blocks = 1
    for j in range(M):
        b = C // ne[j]
        if b + 1 > max_blocks:
            max_blocks = b + 1
    closed_sums = [ [0]*max_blocks for _ in range(M) ]
    closed_len = [0]*M  # cuántos bloques completos tenemos almacenados por j

    best_cost = 10**18
    best_seq = [-1]*C

    start = time.time()
    outfile = argv[1]

    def write_best(cost: int):
        end = time.time()
        with open(outfile, "w") as f:
            print(cost, round(end-start, 1), file=f)
            print(" ".join(map(str, best_seq)), file=f)

    # LB: penalizaciones inevitables acumuladas en bloques completos
    def lower_bound() -> int:
        lb = 0
        for j in range(M):
            cnt = closed_len[j]
            cej = ce[j]
            col = closed_sums[j]
            for t in range(cnt):
                v = col[t]
                if v > cej:
                    lb += (v - cej)
        return lb

    # Backtracking
    def backtrack(pos: int, cost: int):
        nonlocal best_cost

        if cost >= best_cost:
            return

        lb = lower_bound()
        if cost + lb >= best_cost:
            return

        if pos == C:
            best_cost = cost
            for i in range(C):
                best_seq[i] = seq[i]
            write_best(cost)
            return

        for cls in range(K):
            if remaining[cls] == 0:
                continue

            added = 0
            # para restaurar, guardamos:
            old_queue_vals = [0]*M
            closed_now_j = [0]*M        # 1 si cerramos bloque para j, 0 si no
            prev_current = [0]*M        # valor de current_block[j] antes de modificar
            closed_now_count = 0

            # aplicar cls en pos
            for j in range(M):
                idx = pos % ne[j]
                old = win_queue[j][idx]
                old_queue_vals[j] = old

                # guardar prev current block
                prev_current[j] = current_block[j]

                # actualizar ventana circular
                win_count[j] -= old
                add = mill_clas[cls][j]
                win_queue[j][idx] = add
                win_count[j] += add

                # coste instantáneo por la ventana que termina en pos
                if win_count[j] > ce[j]:
                    added += win_count[j] - ce[j]

                # actualizar bloque parcial
                current_block[j] += add - old

                # si cerramos un bloque completo (idx apunta al final)
                if idx + 1 == ne[j]:
                    k = closed_len[j]
                    closed_sums[j][k] = current_block[j]
                    closed_len[j] = k + 1
                    closed_now_j[j] = 1
                    closed_now_count += 1
                    # iniciar nuevo bloque parcial
                    current_block[j] = 0

            # poda por bound con coste incremental exacto
            if cost + added < best_cost:
                seq[pos] = cls
                remaining[cls] -= 1

                backtrack(pos+1, cost + added)

                seq[pos] = -1
                remaining[cls] += 1

            # deshacer: primero revertir bloques cerrados (si los hubo), y restaurar current_block
            # luego revertir ventana circular
            # revertir bloques cerrados
            for j in range(M):
                if closed_now_j[j] == 1:
                    closed_len[j] -= 1
                    # restore current_block to the value it had BEFORE we modified it
                    current_block[j] = prev_current[j]
                else:
                    # si no cerramos, también restauramos current_block
                    current_block[j] = prev_current[j]

            # revertir ventana circular
            for j in range(M):
                idx = pos % ne[j]
                # quitar lo que pusimos
                win_count[j] -= win_queue[j][idx]
                win_queue[j][idx] = old_queue_vals[j]
                win_count[j] += old_queue_vals[j]

    backtrack(0, 0)

    if best_seq[0] == -1:
        with open(outfile, "w") as f:
            print("No solution", file=f)

if __name__ == "__main__":
    solve()
