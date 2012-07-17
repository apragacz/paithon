def mean(values, default=None):
    if values:
        return sum(values) / len(values)
    else:
        return default


def variance(values, default=None):
    if values:
        sum((x ** 2 for x in values)) / len(values) - mean(values) ** 2
    else:
        return default


def mean_and_variance(values, default=None):
    values = list(values)
    return (mean(values, default), variance(values, default))
