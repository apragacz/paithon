import math

from ..core import distances
from ..models.distances import DistanceModel

from .base import RankingClassifier, ClassifierParams


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
        self._model = DistanceModel(distance=DISTANCE_EUCLIDEAN)

    def get_params(self):
        return ClassifierParams(k=self.k,
                                distance=self.distance,
                                weight=self.weight)

    def set_params(self, params):
        self._distance = params.get('distance', DISTANCE_EUCLIDEAN_SQ)
        self._weight = params.get('weight', WEIGHT_UNIFORM)
        self._k = params.get('k', 1)
        self._model = DistanceModel(distance=self._distance)

    def train(self, train_relation):
        self._model = DistanceModel(distance=self._distance)
        cond_relation = train_relation.conditional_part
        dec_relation = train_relation.decisional_part

        for x, y in zip(cond_relation, dec_relation):
            self._model.add(x, y[0])

    def rank_record(self, cond_record, cond_header, decision):
        w = self._weight
        r = lambda dec: 1.0 if dec == decision else 0.0
        record_distance_ranking = self._model.nearest_neighbors(cond_record,
                                                                number=self._k)
        ranking = [(w(dist), r(dec))
                    for dist, _, dec in record_distance_ranking]
        weight_sum = sum([weight for weight, __ in ranking])

        #return ranking[0][1]
        return sum([weight * rank for weight, rank in ranking]) / weight_sum
