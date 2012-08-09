from unittest import TestCase

from paithon.classifiers.measures import (accuracy, true_class_rates, recalls,
    precisions, f1_scores)
from paithon.classifiers.knn import KNNClassifier
from paithon.data.relations.relations import Relation
from paithon.data.relations.readers.csv import SmartCSVReader


class KNNTestCase(TestCase):
    def test_simple(self):
        f = open('tests/iris.txt')
        csv_reader = SmartCSVReader(f, header=True, separator='\t')
        relation = Relation()
        relation.read(csv_reader)
        f.close()
        relation.set_decision_index(4)

        classifier = KNNClassifier(k=1)
        evaluation = classifier.crossvalidate(relation)

        self.assertLess(0.95, accuracy(evaluation))

        self.assertEqual(recalls(evaluation), true_class_rates(evaluation))
        tcr = true_class_rates(evaluation)
        self.assertEqual(1, tcr['setosa'])
        self.assertLessEqual(0.94, tcr['versicolor'])
        self.assertLessEqual(0.92, tcr['virginica'])
        self.assertLess(tcr['versicolor'], 1)
        self.assertLess(tcr['virginica'], 1)

        r = recalls(evaluation)
        p = precisions(evaluation)
        f1 = f1_scores(evaluation)

        for v in p.values():
            self.assertLessEqual(0.92, v)
            self.assertLessEqual(v, 1.0)

        for c, v in f1.iteritems():
            rng = [r[c], p[c]]
            self.assertLessEqual(min(rng), v)
            self.assertLessEqual(v, max(rng))
