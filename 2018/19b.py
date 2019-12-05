from functools import reduce
from itertools import chain, combinations
import operator

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


# N = 996
N = 10685796

def brute(N):
    x = 0
    for i in range(1,N+1):
        for j in range(1,N+1):
            if i*j == N:
                x += i
    return x

def factors(facs):
    x = 0
    for thing in set(powerset(facs)):
        prod = reduce(operator.mul, thing, 1)
        x += prod
    return x

print(brute(996))
# Factors pulled found by `factors` program
print(factors([2, 2, 3, 83]))
print(factors([2, 2, 3, 879283]))
