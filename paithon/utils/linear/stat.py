import math


def pearlson(x1, x2):
    #n = len(x1)
    sum1 = sum(x1)
    sum2 = sum(x2)
    sum_sq1 = sum(x1 ** 2)
    sum_sq2 = sum(x2 ** 2)
    var1 = sum_sq1 - sum1 ** 2
    var2 = sum_sq2 - sum2 ** 2
    dot_product = sum(x1 * x2)

    num = dot_product - (sum1 * sum2)
    den = math.sqrt(var1 * var2)
    return num / den
