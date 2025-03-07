"""
Problem: 1154 - Penguins
URL: https://lightoj.com/problem/penguins

Solution by Pablo Dávila Herrero (https://pablodavila.eu)
"""


def _edmonds_karp(graph, bgraph, i, sink, flow):
    if i == sink:
        return flow

    if flow <= 0:
        return 0

    n = len(graph)

    solution = 0
    for j in range(n):
        capacity = graph[i][j] + bgraph[i][j]

        if capacity <= 0:
            continue

        next_flow = min(flow-solution, capacity)
        graph[i][j] -= next_flow
        partial = _edmonds_karp(graph, bgraph, j, sink, next_flow)

        if partial > 0:
            bgraph[j][i] += partial
            solution += partial
        else:
            graph[i][j] += next_flow

        z = 0

        if solution == flow:
            break

    return solution


def edmonds_karp(graph, source, sink):
    n = len(graph)
    flow = 0
    for i in range(n):
        flow += graph[source][i]

    bgraph = [
        [0 for _ in range(n)]
        for _ in range(n)
    ]
    
    return _edmonds_karp(graph, bgraph, source, sink, flow)


t = int(input())
for tc in range(1, t+1):
    n, d = list(map(float, input().split()))
    n = int(n)

    platforms = []  # n
    graph = [
        [0 for _ in range(2*n + 1)]
        for _ in range(2*n + 1)
    ]

    total_penguins = 0
    for i in range(n):
        xi, yi, penguins, jumps = list(map(int, input().split()))
        platforms.append((xi, yi))
        total_penguins += penguins

        # Edge from the entry node to the exit node
        graph[2*i][2*i + 1] = jumps

        # Edges from the exit node to the entry node of other platforms
        for j in range(i):
            xj, yj = platforms[j]

            if d**2 < (xi-xj)**2 + (yi-yj)**2:
                continue

            graph[2*i + 1][2*j] = float("inf")
            graph[2*j + 1][2*i] = float("inf")

        # Edges from the source node to the entry node
        graph[2*n][2*i] = penguins

    solutions = []
    for i in range(n):
        graph_copy = [[e for e in row] for row in graph]
        if edmonds_karp(graph_copy, 2*n, 2*i) == total_penguins:
            solutions.append(i)

    if not solutions:
        print(f"Case {tc}: -1")
    else:
        print(f"Case {tc}: " + " ".join(map(str, solutions)))
