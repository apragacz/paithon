'''
The vector distances
'''
import math


def manhattan(x1, x2):
    return sum((x2 - x1).abs())


def euclidean_squared(x1, x2):
    return sum((x2 - x1) ** 2)


def euclidean(x1, x2):
    return math.sqrt(sum((x2 - x1) ** 2))


def chebyshev(x1, x2):
    return max((x2 - x1).abs())
