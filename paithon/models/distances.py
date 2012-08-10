from .base import Model


class DistanceModel(Model):

    def __init__(self, distance):
        self._distance = distance
        self._data = []

    def add(self, vector, label):
        self._data.append((vector, label))

    def nearest_neighbors(self, vector, number=1):
        """ returns list of [number] tuples (distance, data_vector, data_label)
        sorted by distance
        """
        dist = lambda vec: self._distance(vec, vector)
        ranking = []
        #iterate only over first [number] elements
        it = iter(self._data)
        for _, (vec, label) in zip(range(number), it):
            ranking.append((dist(vec), vec, label))

        ranking.sort(key=lambda el: el[0])

        dist_threshold = ranking[-1][0]

        #remaining iterations
        for (vec, label) in it:
            new_dist = dist(vec)
            if new_dist < dist_threshold:
                #TODO: do it smarter way
                ranking.append((new_dist, vec, label))
                ranking.sort(key=lambda el: el[0])
                ranking.pop()
                dist_threshold = ranking[-1][0]

        return ranking
