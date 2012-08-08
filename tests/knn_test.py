from unittest import TestCase
from paithon.data.relations.relations import Relation
from paithon.data.relations.readers.csv import SmartCSVReader
from paithon.classifiers.knn import KNNClassifier


class KNNTestCase(TestCase):
    def test_simple(self):
        f = open('tests/iris.txt')
        csv_reader = SmartCSVReader(f, header=True, separator='\t')
        relation = Relation()
        relation.read(csv_reader)
        f.close()
        relation.set_decision_index(4)
        classifier = KNNClassifier()
        evaluation = classifier.crossvalidate(relation)
