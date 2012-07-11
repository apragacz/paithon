from collections import defaultdict

from paithon.utils.core import AbstractMethodError
from paithon.utils.progressors import TaskProgressBroadcaster


class ClassifierParams(dict):
    pass


TASK_CLASSIFY = 'classifier_classify'
TASK_CV_TRAIN = 'classifier_crossvalidation_train'
TASK_CV_TEST = 'classifier_crossvalidation_test'
TASK_RANKING = 'classifier_ranking_calculation'


class Classifier(TaskProgressBroadcaster):
    def __init__(self, table=None, decision_index=0, **kwargs):
        super(Classifier).__init__()
        self.init(**kwargs)
        if table is not None:
            self.train(table, decision_index)

    def init(self):
        pass

    def get_params(self):
        return ClassifierParams()

    def set_params(self, params):
        pass

    def train(self, table, decision_index=0):
        raise AbstractMethodError()

    def classify_record(self, record, header):
        raise AbstractMethodError()

    def decisions(self, table):
        self.trigger_task_start(len(table), TASK_CLASSIFY)
        for i, record in enumerate(table):
            yield self.classify_record(record, table.header)
            self.trigger_task_progress(i + 1, TASK_CLASSIFY)
        self.trigger_task_end(TASK_CLASSIFY)

    def crossvalidate(self, table, fold_number=10, decision_index=0):
        parts = table.split_into_parts(fold_number)
        print parts
        evaluation = defaultdict(lambda: defaultdict(int))
        classifier = self
        for i in range(fold_number):
            test_table = parts[i]
            self.trigger_task_start(len(test_table), TASK_CV_TRAIN, (i + 1))
            train_tables = [part for j, part in enumerate(parts) if j != i]
            train_table = table.join_tables(*train_tables)
            classifier.train(train_table, decision_index=decision_index)
            self.trigger_task_end(TASK_CV_TRAIN)
            self.trigger_task_start(len(test_table), TASK_CV_TEST, (i + 1))
            decisions = classifier.decisions(test_table)
            for j, ((__, y), c) in enumerate(zip(test_table, decisions)):
                evaluation[y[decision_index]][c] += 1
            self.trigger_task_end(TASK_CV_TEST)

        return evaluation


class BinaryClassifier(Classifier):
    def __init__(self, table=None, threshold=0.5,
                    positive_decision=1, negative_decision=0,
                    decision_index=0, **kwargs):
        self.threshold = threshold
        self.positive_decision = 1
        self.negative_decision = 0
        super(BinaryClassifier, self).__init__(table=table,
                                                decision_index=decision_index,
                                                **kwargs)

    def rank_record(self, record, header):
        raise AbstractMethodError()

    def classify_record(self, record, header):
        return (self.positive_decision
                    if self.rank_record(record, header) >= self.threshold
                    else self.negative_decision)

    def ranking(self, table):
        self.trigger_task_start(len(table), TASK_RANKING)
        for i, record in enumerate(table):
            yield self.rank_record(record, table.header)
            self.trigger_task_progress(i + 1, TASK_RANKING)
        self.trigger_task_end(TASK_RANKING)

    def full_ranking(self, table):
        return sorted(zip(self.ranking(table),
                            enumerate(table)),
                        key=lambda el: el[0])

    def full_rankings(self, table, params_list):
        start_params = self.get_params()
        for params in params_list:
            self.set_params(params)
            yield self.full_ranking(table)
        self.set_params(start_params)
