from collections import defaultdict

from paithon.core.exceptions import AbstractMethodError
from paithon.core.events import EventDispatcherMixin
from paithon.core.taskinfos import TaskInfo, EVENT_TASK_INFO_CREATED


class ClassifierParams(dict):
    pass


TASK_TRAIN = 'classifier_train'
TASK_CLASSIFY = 'classifier_classify'
TASK_CV = 'classifier_crossvalidation'
TASK_CV_TRAIN = 'classifier_crossvalidation_train'
TASK_CV_TEST = 'classifier_crossvalidation_test'
TASK_RANKING = 'classifier_ranking_calculation'


class Classifier(EventDispatcherMixin):
    def __init__(self, table=None, **kwargs):
        super(Classifier, self).__init__()
        self._params = ClassifierParams()
        self.init(**kwargs)
        if table is not None:
            self.train(table)

    def init(self, **kwargs):
        pass

    def get_params(self):
        return self._params

    def set_params(self, params):
        self._params = params

    def train(self, table):
        raise AbstractMethodError()

    def classify_record(self, record, header):
        raise AbstractMethodError()

    def classify(self, table):
        task_info = TaskInfo(TASK_CLASSIFY, len(table))
        self.trigger_ev(EVENT_TASK_INFO_CREATED, task_info=task_info)
        task_info.signal_start()
        for i, record in enumerate(table):
            yield self.classify_record(record, table.header)
            task_info.signal_progress(i + 1)
        task_info.signal_end()

    def crossvalidate(self, table, fold_number=10):
        cv_task_info = TaskInfo(TASK_CV, fold_number)
        self.trigger_ev(EVENT_TASK_INFO_CREATED, task_info=cv_task_info)
        parts = table.split_into_parts(fold_number)
        evaluation = defaultdict(lambda: defaultdict(int))
        classifier = self
        cv_task_info.signal_start()
        for i in range(fold_number):
            test_table = parts[i]
            train_tables = [part for j, part in enumerate(parts) if j != i]
            train_table = table.join_tables(*train_tables)

            train_task_info = TaskInfo(TASK_CV_TRAIN, len(train_table),
                                        {'phase': i + 1})
            self.trigger_ev(EVENT_TASK_INFO_CREATED, task_info=train_task_info)
            train_task_info.signal_begin()
            classifier.train(train_table)
            train_task_info.signal_end()

            test_task_info = TaskInfo(TASK_CV_TEST, len(test_table),
                                        {'phase': i + 1})
            self.trigger_ev(EVENT_TASK_INFO_CREATED, task_info=test_task_info)
            test_task_info.signal_start()
            decisions = classifier.classify(test_table)
            for j, ((__, y), c) in enumerate(zip(test_table, decisions)):
                evaluation[y[0]][c] += 1
                test_task_info.signal_progress(j + 1)
            test_task_info.signal_end()
            cv_task_info.signal_progress(i + 1)

        cv_task_info.signal_end()
        return evaluation


class BinaryClassifier(Classifier):
    def __init__(self, table=None, threshold=0.5,
                    positive_decision=1, negative_decision=0,
                    **kwargs):
        self.threshold = threshold
        self.positive_decision = 1
        self.negative_decision = 0
        super(BinaryClassifier, self).__init__(table=table, **kwargs)

    def rank_record(self, record, header):
        raise AbstractMethodError()

    def classify_record(self, record, header):
        return (self.positive_decision
                    if self.rank_record(record, header) >= self.threshold
                    else self.negative_decision)

    def ranking(self, table):
        ranking_task_info = TaskInfo(TASK_RANKING, len(table))
        self.trigger_ev(EVENT_TASK_INFO_CREATED, task_info=ranking_task_info)
        ranking_task_info.signal_start()
        for i, record in enumerate(table):
            yield self.rank_record(record, table.header)
            ranking_task_info.signal_progress(i + 1)
        ranking_task_info.signal_end()

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
