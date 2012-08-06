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
    def __init__(self, train_table=None, **kwargs):
        super(Classifier, self).__init__()
        self.initialize()
        self.set_params(kwargs)
        if train_table is not None:
            self.train(train_table)

    def initialize(self):
        raise AbstractMethodError()

    def get_params(self):
        raise AbstractMethodError()

    def set_params(self, params):
        raise AbstractMethodError()

    def train(self, train_table):
        raise AbstractMethodError()

    def classify_record(self, record, header):
        raise AbstractMethodError()

    def iter_classify(self, test_table):
        task_info = TaskInfo(TASK_CLASSIFY, len(test_table))
        self.trigger_ev(EVENT_TASK_INFO_CREATED, task_info=task_info)
        task_info.signal_start()
        for i, record in enumerate(test_table):
            yield self.classify_record(record, test_table.header)
            task_info.signal_progress(i + 1)
        task_info.signal_end()

    def classify(self, test_table):
        return list(self.iter_classify(test_table))

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


class RankingClassifier(Classifier):

    def rank_record(self, record, header, decision):
        raise AbstractMethodError()

    def classify_record(self, record, header):
        assert(header.values)
        ranking = [(self.rank_record(record, header, decision), decision)
                    for decision in header.values]
        return max(ranking, key=lambda x: x[0])[1]

    def iter_rank(self, test_table, decision):
        ranking_task_info = TaskInfo(TASK_RANKING, len(test_table))
        self.trigger_ev(EVENT_TASK_INFO_CREATED, task_info=ranking_task_info)
        ranking_task_info.signal_start()
        for i, record in enumerate(test_table):
            yield self.rank_record(record, test_table.header, decision)
            ranking_task_info.signal_progress(i + 1)
        ranking_task_info.signal_end()

    def rank(self, test_table):
        return list(self.iter_rank())

    def ranking(self, test_table, decision, sort=True):
        result = [(i, rank)
                    for rank, i in zip(self.iterrank(test_table, decision),
                                                    xrange(len(test_table)))]
        if sort:
            return sorted(result, key=lambda el: el[1])
        else:
            return result
