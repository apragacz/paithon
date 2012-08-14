import math
from collections import Counter


def collection(x):
    if hasattr(x, '__len__'):
        return x
    else:
        return tuple(x)


def mean(values):
    assert(values)
    values = collection(values)
    return sum(values) / len(values)


def variance(values):
    assert(values)
    values = collection(values)
    return sum((x ** 2 for x in values)) / len(values) - mean(values) ** 2


def mean_and_variance(values):
    values = collection(values)
    return (mean(values), variance(values))


def covariance(values1, values2):
    assert(values1)
    assert(values2)
    values1 = collection(values1)
    values2 = collection(values2)
    dot_product = sum((x * y for x, y in zip(values1, values2)))
    return dot_product / len(values1) - mean(values1) * mean(values2)


def pearson_correlation(values1, values2):
    values1 = collection(values1)
    values2 = collection(values2)
    sum1 = sum(values1)
    sum2 = sum(values2)
    n = len(values1)
    sum_sq1 = sum((x ** 2 for x in values1))
    sum_sq2 = sum((x ** 2 for x in values2))
    var1 = n * sum_sq1 - sum1 ** 2
    var2 = n * sum_sq2 - sum2 ** 2
    dot_product = sum((x1 * x2 for x1, x2 in zip(values1, values2)))

    num = n * dot_product - (sum1 * sum2)
    den = math.sqrt(var1 * var2)

    return num / den


def distribution(values):
    distribution = {}
    c = Counter(values)
    total_counter = float(sum((counter for _, counter in  c.most_common())))
    for value, counter in c.most_common():
        distribution[value] = counter / total_counter
    return distribution


def distribution_entropy(distribution, r=2):
    return - sum((math.log(p, r) * p for p in distribution.values()))


def distribution_gini(distribution):
    return 1 - sum((p ** 2 for p in distribution.values()))


def entropy(values, r=2):
    return distribution_entropy(distribution(values), r=r)


def gini(values):
    return distribution_gini(distribution(values))
