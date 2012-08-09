def accuracy(evaluation):
    classes = evaluation.keys()
    correct_counter = 0
    total_counter = 0
    for true_class in classes:
        for classified_class in classes:
            counter = evaluation[true_class][classified_class]
            if true_class == classified_class:
                correct_counter += counter
            total_counter += counter
    return correct_counter / float(total_counter)


def true_class_rates(evaluation):
    classes = evaluation.keys()
    tcr = {}
    for true_class in classes:
        correct_counter = 0
        total_counter = 0
        for classified_class in classes:
            counter = evaluation[true_class][classified_class]
            if true_class == classified_class:
                correct_counter += counter
            total_counter += counter
        tcr[true_class] = correct_counter / float(total_counter)
    return tcr


def recalls(evaluation):
    return true_class_rates(evaluation)


def precisions(evaluation):
    classes = evaluation.keys()
    p = {}
    for classified_class in classes:
        correct_counter = 0
        total_counter = 0
        for true_class in classes:
            counter = evaluation[true_class][classified_class]
            if true_class == classified_class:
                correct_counter += counter
            total_counter += counter
        p[classified_class] = correct_counter / float(total_counter)
    return p


def f1_scores(evaluation):
    classes = evaluation.keys()
    p = precisions(evaluation)
    r = recalls(evaluation)
    f1 = {}
    for c in classes:
        f1[c] = 2 * p[c] * r[c] / (p[c] + r[c])
    return f1
