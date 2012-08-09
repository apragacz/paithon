from unittest import TestCase

from paithon.classifiers.base import Classifier, RankingClassifier


class ClassifierCase(TestCase):
    def test_simple(self):
        self.assertRaises(TypeError, lambda: Classifier())
        self.assertRaises(TypeError, lambda: RankingClassifier())
