import random

from ..models.perceptons import PerceptonLayeredNetwork

from .base import RankingClassifier, ClassifierParams


class NeuralNetworkClassifier(RankingClassifier):

    def initialize(self):
        self._outputs = None

    def get_params(self):
        return ClassifierParams(n=self._n)

    def set_params(self, params):
        self._n = params.get('n', 100)
        self._rnd = params.get('rnd', random.Random())
        self._threshold_function = params.get('threshold_function', None)
        self._threshold_derivative_function = params.get(
                                        'threshold_derivative_function', None)
        self._learning_rate = params.get('learning_rate', 0.01)
        self._model = PerceptonLayeredNetwork(1, 1,
                num_of_immediate_elements_list=[self._n], rnd=self._rnd,
                threshold_function=self._threshold_function,
                threshold_derivative_function=self._threshold_derivative_function)

    def train(self, train_relation):
        cond_relation = train_relation.conditional_part
        dec_relation = train_relation.decisional_part
        num_of_inputs = len(cond_relation.attributes)
        self._decisions = dec_relation.attributes[0].values
        num_of_outputs = len(self._decisions)
        self._model = PerceptonLayeredNetwork(num_of_inputs, num_of_outputs,
                num_of_immediate_elements_list=[self._n], rnd=self._rnd,
                threshold_function=self._threshold_function,
                threshold_derivative_function=self._threshold_derivative_function)

        #TODO: train backpropagation
        #FIXME: additional "1" param

        #cond_dec_records = train_relation.iter_conditional_decisional_records()

        #for x, y in zip(cond_relation, dec_relation):
        #    self._model.add(x, y[0])

    def classify_rank_begin(self, cond_record, cond_header, dec_header):
        self._outputs = self._model.outputs(cond_record)

    def classify_rank_end(self, cond_record, cond_header, dec_header):
        self._outputs = None

    def rank_record(self, cond_record, cond_header, decision):
        #TODO: rank record
        pass
