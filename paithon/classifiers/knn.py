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
        self._train_cond_relation = []
        self._train_dec_relation = []

    def get_params(self):
        return ClassifierParams(k=self.k,
                                distance=self.distance,
                                weight=self.weight)

    def set_params(self, params):
        self._distance = params.get('distance', DISTANCE_EUCLIDEAN_SQ)
        self._weight = params.get('weight', WEIGHT_UNIFORM)
        self._k = params.get('k', 1)

    def train(self, train_relation):
        self._train_cond_relation = train_relation.conditional_part
        self._train_dec_relation = train_relation.decisional_part

    def record_distance_ranking(self, cond_record):
        dist = lambda cond_rec: self._distance(cond_record, cond_rec)
        it = iter(zip(self._train_cond_relation, self._train_dec_relation))
        ranking = []
        for _, (cond_rec, dec_rec) in zip(range(self._k), it):
            ranking.append((dist(cond_rec), cond_rec, dec_rec[0]))

        ranking.sort(key=lambda el: el[0])

        dist_threshold = ranking[-1][0]
        for (cond_rec, dec_rec) in it:
            rec_dist = dist(cond_rec)
            if rec_dist < dist_threshold:
                ranking.append((rec_dist, cond_rec, dec_rec[0]))
                ranking.sort(key=lambda el: el[0])
                ranking.pop()
                dist_threshold = ranking[-1][0]

        return ranking

    def rank_record(self, cond_record, cond_header, decision):
        w = self._weight
        r = lambda dec: 1.0 if dec == decision else 0.0
        record_distance_ranking = self.record_distance_ranking(cond_record)
        ranking = [(w(dist), r(dec))
                    for dist, _, dec in record_distance_ranking]
        weight_sum = sum([weight for weight, __ in ranking])

        #return ranking[0][1]
        return sum([weight * rank for weight, rank in ranking]) / weight_sum
