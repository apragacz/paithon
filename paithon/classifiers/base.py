from abc import ABCMeta, abstractmethod
from collections import defaultdict

from ..core.events import EventDispatcherMixin
from ..core.taskinfos import TaskInfo, EVENT_TASK_INFO_CREATED


class ClassifierParams(dict):
    pass


TASK_TRAIN = 'classifier_train'
TASK_CLASSIFY = 'classifier_classify'
TASK_CV = 'classifier_crossvalidation'
TASK_CV_TRAIN = 'classifier_crossvalidation_train'
TASK_CV_TEST = 'classifier_crossvalidation_test'
TASK_RANKING = 'classifier_ranking_calculation'


class Classifier(EventDispatcherMixin):

    __metaclass__ = ABCMeta

    def __init__(self, train_relation=None, **kwargs):
        super(Classifier, self).__init__()
        self.initialize()
        self.set_params(kwargs)
        if train_relation is not None:
            self.train(train_relation)

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def get_params(self):
        pass

    @abstractmethod
    def set_params(self, params):
        pass

    @abstractmethod
    def train(self, train_relation):
        pass

    @abstractmethod
    def classify_record(self, cond_record, cond_header, dec_header):
        pass

    def iter_classify(self, test_relation):
        task_info = TaskInfo(TASK_CLASSIFY, len(test_relation))
        self.trigger_ev(EVENT_TASK_INFO_CREATED, task_info=task_info)
        task_info.signal_start()
        test_conditional_relation = test_relation.conditional_part
        test_conditional_header = test_conditional_relation.header
        test_decisional_header = test_relation.decisional_part.header
        for i, record in enumerate(test_conditional_relation):
            yield self.classify_record(record, test_conditional_header,
                                        test_decisional_header)
            task_info.signal_progress(i + 1)
        task_info.signal_end()

    def classify(self, test_relation):
        return list(self.iter_classify(test_relation))

    def crossvalidate(self, relation, fold_number=10):
        cv_task_info = TaskInfo(TASK_CV, fold_number)
        self.trigger_ev(EVENT_TASK_INFO_CREATED, task_info=cv_task_info)
        parts = relation.split_into_parts(fold_number)
        evaluation = defaultdict(lambda: defaultdict(int))
        classifier = self
        cv_task_info.signal_start()
        for i in range(fold_number):
            test_relation = parts[i]
            train_relations = [part for j, part in enumerate(parts) if j != i]
            train_relation = relation.join_tables(*train_relations)

            train_task_info = TaskInfo(TASK_CV_TRAIN, len(train_relation),
                                        {'phase': i + 1})
            self.trigger_ev(EVENT_TASK_INFO_CREATED, task_info=train_task_info)
            train_task_info.signal_start()
            classifier.train(train_relation)
            train_task_info.signal_end()

            test_task_info = TaskInfo(TASK_CV_TEST, len(test_relation),
                                        {'phase': i + 1})
            self.trigger_ev(EVENT_TASK_INFO_CREATED, task_info=test_task_info)
            test_task_info.signal_start()

            test_decisional_relation = test_relation.decisional_part

            decisions = classifier.classify(test_relation)
            for j, (y, c) in enumerate(zip(test_decisional_relation,
                                                decisions)):
                evaluation[y[0]][c] += 1
                test_task_info.signal_progress(j + 1)
            test_task_info.signal_end()
            cv_task_info.signal_progress(i + 1)

        cv_task_info.signal_end()
        return evaluation


class RankingClassifier(Classifier):

    __metaclass__ = ABCMeta

    @abstractmethod
    def rank_record(self, cond_record, cond_header, decision):
        pass

    def classify_record(self, cond_record, cond_header, dec_header):
        assert(len(dec_header.attributes) == 1)
        dec_attr = dec_header.attributes[0]
        assert(dec_attr.discrete)
        assert(dec_attr.values)
        ranking = [(self.rank_record(cond_record, cond_header, decision),
                        decision)
                    for decision in dec_attr.values]
        return max(ranking, key=lambda x: x[0])[1]

    def iter_rank(self, test_relation, decision):
        ranking_task_info = TaskInfo(TASK_RANKING, len(test_relation))
        self.trigger_ev(EVENT_TASK_INFO_CREATED, task_info=ranking_task_info)
        ranking_task_info.signal_start()
        cond_relation = test_relation.conditional_part
        cond_header = cond_relation.header
        for i, record in enumerate(cond_relation):
            yield self.rank_record(record, cond_header, decision)
            ranking_task_info.signal_progress(i + 1)
        ranking_task_info.signal_end()

    def rank(self, test_relation, decision):
        return list(self.iter_rank(test_relation, decision))

    def ranking(self, test_relation, decision, sort=True):
        result = [(i, rank)
                    for rank, i in zip(self.iterrank(test_relation, decision),
                                                    xrange(len(test_relation)))]
        if sort:
            return sorted(result, key=lambda el: el[1])
        else:
            return result
