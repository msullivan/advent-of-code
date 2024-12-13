# Stuff that I might want to copy out and reuse

import operator
OPS = {
    x.__doc__.split()[3]: x
    for k in dir(operator)
    if not k.startswith('__')
    and (x := getattr(operator, k)).__doc__.startswith("Same as a ")
}


def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)

    l = ""
    # XXX: add reversed if needed
    for y in list((range(miny, maxy+1))):
        for x in range(minx, maxx+1):
            l += painted.get((x,y), ".")
        l += "\n"
    print(l)


import heapq
# This is A* if you pass a heuristic and a target, otherwise Dijkstra's
# edges should return a sequence of (nbr, weight) pairs
def dijkstra(m, edges, start, heuristic=None, target=None):
    cost = {start: 0}
    path = {}
    todo = [(0, 0, start)]
    explored = 0

    while todo and todo[0][-1] != target:
        _, k, cur = heapq.heappop(todo)
        if k != cost[cur]:
            continue
        explored += 1

        nbrs = list(edges(m, cur))
        for nbr, weight in nbrs:
            ncost = cost[cur] + weight
            if nbr not in cost or ncost < cost[nbr]:
                cost[nbr] = ncost
                path[nbr] = cur
                hcost = ncost if not heuristic else ncost + heuristic(nbr)
                heapq.heappush(todo, (hcost, ncost, nbr))

    return cost, path


def binary_search(pred, lo, hi=None):
    """Finds the first n in [lo, hi) such that pred(n) holds.

    hi == None -> infty
    """
    assert not pred(lo)

    if hi is None:
        hi = max(lo, 1)
        while not pred(hi):
            hi *= 2

    assert pred(hi)

    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1

    return lo


if False:
    #### Read grid
    m = defaultdict(lambda: '.')
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            m[x,y] = c


    # DFS
    seen = set()
    q = [start]
    while q:
        node = q.pop()
        for _, nbr in gnbrs(node):  # ??
            if (
                nbr not in seen
                # and ...
            ):
                q.append(nbr)
                seen.add(nbr)


    # BFS
    seen = set()
    q = collections.deque([start])
    while q:
        node = q.popleft()
        for _, nbr in gnbrs(node):  # ??
            if (
                nbr not in seen
                # and ...
            ):
                q.append(nbr)
                seen.add(nbr)
