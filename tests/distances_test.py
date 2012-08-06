from paithon.core.distances import (chebyshev, euclidean, euclidean_squared,
    manhattan)
from unittest import TestCase


class DistancesTest(TestCase):

    def test_simple(self):
        x = (1, 2, 5)
        y = (3, 8, 8)

        self.assertEqual(chebyshev(x, x), 0)
        self.assertEqual(euclidean(x, x), 0)
        self.assertEqual(euclidean_squared(x, x), 0)
        self.assertEqual(manhattan(x, x), 0)

        self.assertEqual(chebyshev(x, y), 6)
        self.assertEqual(euclidean(x, y), 7)
        self.assertEqual(euclidean_squared(x, y), 49)
        self.assertEqual(manhattan(x, y), 11)

        self.assertEqual(chebyshev(y, x), 6)
        self.assertEqual(euclidean(y, x), 7)
        self.assertEqual(euclidean_squared(y, x), 49)
        self.assertEqual(manhattan(y, x), 11)
