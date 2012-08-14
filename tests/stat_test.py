import math
from unittest import TestCase

from paithon.core.stat import (mean, variance, mean_and_variance, entropy, gini,
    pearson_correlation, covariance)


class StatTestCase(TestCase):

    def test_simple(self):
        def seqiter1():
            return iter([1, 5, 9, 5])

        def seqiter2():
            return iter([1, 1, 1, 1])

        def seqiter3():
            return iter([1, 2, 3, 4])

        self.assertEqual(mean(seqiter1()), 5)
        self.assertEqual(variance([1, 5, 9, 5]), 8)
        self.assertEqual(variance((1, 5, 9, 5)), 8)
        self.assertEqual(variance(seqiter1()), 8)
        self.assertEqual(mean_and_variance(seqiter1()), (5, 8))
        self.assertEqual(covariance(seqiter1(), seqiter1()), 8)
        self.assertEqual(covariance((1, 5, 9, 5), (1, 5, 9, 5)), 8)
        self.assertEqual(covariance((1, 5, 9, 5), (-1, -5, -9, -5)), -8)

        self.assertEqual(gini(seqiter2()), 0.0)
        self.assertEqual(gini(seqiter1()), 0.625)
        self.assertEqual(gini(seqiter3()), 0.75)

        self.assertEqual(entropy(seqiter2()), 0)
        self.assertEqual(entropy(seqiter3()), math.log(4, 2))

        x1 = (1, 4, 5)
        x2 = (-1, -4, -5)
        self.assertEqual(pearson_correlation(x1, x1), 1)
        self.assertEqual(pearson_correlation(x1, x2), -1)
