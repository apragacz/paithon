import math

from paithon.classifiers.base import RankingClassifier, ClassifierParams
from paithon.core import distances

DISTANCE_EUCLIDEAN_SQ = distances.euclidean_squared
DISTANCE_EUCLIDEAN = distances.euclidean
DISTANCE_CHEBYSHEV = distances.chebyshev
DISTANCE_MANHATTAN = distances.manhattan


WEIGHT_UNIFORM = lambda dist: 1.0
WEIGHT_INVERTED = lambda dist: 1.0 / (1.0 + dist)
WEIGHT_EXPONENTIAL = lambda dist: math.exp(-dist)
WEIGHT_EXPONENTIAL_SQRT = lambda dist: math.exp(-math.sqrt(dist))
WEIGHT_INVERTED_SQRT = lambda dist: 1.0 / (1.0 + math.sqrt(dist))
WEIGHT_ONE_MINUS = lambda dist: 1.0 - dist  # only for distances in range [0,1]


class KNNClassifier(RankingClassifier):
    def initialize(self):
        self._train_conditional_relation = []
        self._train_decisional_relation = []

    def get_params(self):
        return ClassifierParams(k=self.k,
                                distance=self.distance,
                                weight=self.weight)

    def set_params(self, params):
        self._distance = params.get('distance', DISTANCE_EUCLIDEAN_SQ)
        self._weight = params.get('weight', WEIGHT_UNIFORM)
        self._k = params.get('k', 1)

    def train(self, train_relation):
        self._train_conditional_relation = train_relation.conditional_part
        self._train_decisional_relation = train_relation.decisonal_part

    def record_distance_ranking(self, record, header):
        x1, y1 = record
        dist = lambda rec: self._distance(x1, rec[0])
        table_iter = iter(self._knn_train_records)
        ranking = []
        for __, rec in zip(range(self._k), table_iter):
            ranking.append((dist(rec), rec))

        ranking.sort(key=lambda el: el[0])

        dist_threshold = ranking[-1][0]
        for rec in table_iter:
            rec_dist = dist(rec)
            if rec_dist < dist_threshold:
                ranking.append((rec_dist, rec))
                ranking.sort(key=lambda el: el[0])
                ranking.pop()
                dist_threshold = ranking[-1][0]

        return ranking

    def rank_record(self, record, header):
        x1, y1 = record
        w = self.weight
        r = lambda rec: 1.0 if rec[1][self.decision_index] == self.positive_decision else 0.0
        record_distance_ranking = self.record_distance_ranking(record, header)
        ranking = [(w(dist), r(rec))
                    for dist, rec in record_distance_ranking]
        weight_sum = sum([weight for weight, __ in ranking])

        #return ranking[0][1]
        return sum([weight * rank for weight, rank in ranking]) / weight_sum
