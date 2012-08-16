from ..core.stat import entropy
from ..models.trees import DecisionTree

from .base import Classifier, ClassifierParams


class TreeClassifier(Classifier):
    def initialize(self):
        self._disortion_measure = entropy
        self._model = DecisionTree(self._disortion_measure)

    def get_params(self):
        return ClassifierParams(disortion_measure=self._disortion_measure)

    def set_params(self, params):
        self._disortion_measure = params.get('disortion_measure', entropy)
        self._model = DecisionTree(self._disortion_measure)

    def train(self, train_relation):
        self._model = DecisionTree(self._disortion_measure)
        cond_attributes = train_relation.conditional_part.attributes
        cond_dec_records = train_relation.iter_conditional_decisional_records()

        self._model.build(cond_dec_records, cond_attributes)

    def classify_record(self, cond_record, cond_header, dec_header):
        return self._model.decision(cond_record)
