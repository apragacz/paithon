import math


def euclidean(x1, x2):
    return math.sqrt(sum([(e1 - e2) ** 2 for e1, e2 in zip(x1, x2)]))


def chebyshev(x1, x2):
    return max([abs(e1 - e2) for e1, e2 in zip(x1, x2)])


def manhattan(x1, x2):
    return sum([abs(e1 - e2) for e1, e2 in zip(x1, x2)])


def euclidean_squared(x1, x2):
    "euclidean distance squared"
    return sum([(e1 - e2) ** 2 for e1, e2 in zip(x1, x2)])
