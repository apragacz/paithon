from unittest import TestCase
from paithon.data.relations.relations import Relation
from paithon.data.relations.readers.csv import (RecordNominalCSVReader,
    SmartCSVReader)

csv_file_data1 = """attr,attr2,attr3
1,2,Y
2,4,Y
3,4,N
5,2,N
6,4,N"""


class ReadableFileMock(object):
    def __init__(self, data):
        self._data = data
        self._datalines = data.split('\n')
        self._pos = data

    def readline(self):
        if self._datalines:
            return '%s\n' % self._datalines.pop(0)
        else:
            return ''


class RelationsTestCase(TestCase):

    def setUp(self):
        pass

    def test_simple(self):
        f = ReadableFileMock(csv_file_data1)
        csv_reader = RecordNominalCSVReader(f, header=True)
        relation = Relation()
        relation.read(csv_reader)
        self.assertSetEqual(relation.attributes[2].values,
            set(['Y', 'N']))
        self.assertEqual(relation[1], ('2', '4', 'Y'))
        self.assertEqual(len(relation), 5)
        relation2 = relation[1:3]
        self.assertIsInstance(relation2, Relation)
        self.assertEqual(relation2[1], ('3', '4', 'N'))
        self.assertEqual(len(relation.sample_without_replacement(2)), 2)
        self.assertEqual(len(relation.sample_with_replacement(2)), 2)

        split1 = relation.split_by_column_values(0)
        self.assertEqual(len(split1), 5)

        split2 = relation.split_by_column_values(1)
        self.assertEqual(len(split2), 2)
        self.assertEqual(len(split2['2']), 2)
        self.assertEqual(len(split2['4']), 3)

        split3 = relation.split_by_column_values(2)
        self.assertEqual(len(split3), 2)
        self.assertEqual(len(split3['Y']), 2)
        self.assertEqual(len(split3['N']), 3)

        self.assertListEqual(relation.attribute_values(0),
                                ['1', '2', '3', '5', '6'])
        self.assertListEqual(relation.attribute_values(2),
                                ['Y', 'Y', 'N', 'N', 'N'])

    def test_iris(self):
        f = open('tests/iris.txt')
        csv_reader = SmartCSVReader(f, header=True, separator='\t')
        relation = Relation()
        relation.read(csv_reader)
        f.close()
        self.assertEqual(len(relation), 150)
        self.assertEqual(len(relation.attributes), 9)

        self.assertTrue(relation.attributes[0].numeric)
        self.assertEqual(relation.attributes[4].name, 'Species')
        for attribute in relation.attributes:
            if attribute.name == 'Species':
                self.assertFalse(attribute.numeric)
                self.assertTrue(attribute.discrete)
                self.assertSetEqual(attribute.values,
                                    set(["setosa", "versicolor", "virginica"]))
            else:
                self.assertTrue(attribute.numeric)
                self.assertFalse(attribute.discrete)
        self.assertTrue(relation.attributes[8].numeric)

        relation.set_decision_index(4)

        cond_relation = relation.conditional_part
        dec_relation = relation.decisional_part

        self.assertEqual(len(cond_relation), 150)
        self.assertEqual(len(cond_relation.attributes), 8)
        self.assertEqual(len(dec_relation), 150)
        self.assertEqual(len(dec_relation.attributes), 1)

        for attribute in cond_relation.attributes:
            self.assertTrue(attribute.numeric)
            self.assertFalse(attribute.discrete)

        for attribute in dec_relation.attributes:
            self.assertFalse(attribute.numeric)
            self.assertTrue(attribute.discrete)
            self.assertSetEqual(attribute.values,
                                set(["setosa", "versicolor", "virginica"]))
