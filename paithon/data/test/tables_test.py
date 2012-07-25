from unittest import TestCase
from paithon.data.tables.tables import Table
from paithon.data.tables.readers.csv import (RecordNumericCSVReader,
    RecordNominalCSVReader)

csv_file_data1 = """attr,attr2,attr3
1,2,Y
2,4,Y
3,4,N
5,2,N
6,4,N"""


class FileMock(object):
    def __init__(self, data):
        self._data = data
        self._datalines = data.split('\n')
        self._pos = data

    def readline(self):
        if self._datalines:
            return '%s\n' % self._datalines.pop(0)
        else:
            return ''


class TablesTestCase(TestCase):

    def setUp(self):
        self.f = FileMock(csv_file_data1)

    def test_simple(self):
        csv_reader = RecordNominalCSVReader(self.f, header=True)
        table = Table()
        table.read(csv_reader)
        self.assertEqual(table[1], ('2', '4', 'Y'))
        self.assertEqual(len(table), 5)
        table2 = table[1:3]
        self.assertIsInstance(table2, Table)
        self.assertEqual(table2[1], ('3', '4', 'N'))
        self.assertEqual(len(table.sample_without_replacement(2)), 2)
        self.assertEqual(len(table.sample_with_replacement(2)), 2)
