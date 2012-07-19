import random
from collections import defaultdict
from paithon.data.tables.headers import Header


class Table(object):
    def __init__(self, header=None):
        self._data = []
        self._header = header if header is not None else Header()
        self._decision_index = None

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        print key
        return self._data[key]

    def set_decision_index(self, index):
        self._decision_index = index

    def set_header(self, header):
        self._header = header

    def add_record(self, record):
        self._data.append(record)

    def reload_header(self):
        self._header = Header()
        self.reload_header_values()

    def reload_header_values(self):
        if self._data:
            self._header._columns_values = [set() for _ in self._data[0]]

            for record in self.data:
                for i, item in enumerate(record):
                    self._header._columns_values[i].add(item)

    def read(self, reader):
        self._data = []
        self.set_header(reader.read_header())
        for record in reader:
            self.add_record(record)
        self._header.load_values(self)

    def write(self, writer):
        writer.write_header(self._header)
        for record in self._data:
            writer.write_record(record)

    def split_by_column_values(self, column_index, table_class=None):
        if table_class is None:
            table_class = self.__class__
        sp = defaultdict(lambda: table_class(header=self._header))

        for record in self.data:
            sp[record[column_index]].add_record(record)

        return sp

    def split_into_parts(self, part_number=10, table_class=None):
        if table_class is None:
            table_class = self.__class__
        parts = [table_class(header=self._header) for i in range(part_number)]

        for i, record in enumerate(self._data):
            parts[i % part_number].add_record(record)

        return parts

    def sample_with_replacement(self, sample_number, rnd=None,
            table_class=None):
        if table_class is None:
            table_class = self.__class__
        if rnd is None:
            rnd = random.Random()

        table = table_class(header=self._header)
        data_len = len(self._data)

        for __ in xrange(sample_number):
            table.add_record(self._data[rnd.randrange(0, data_len)])

        return table

    def sample_without_replacement(self, sample_number, rnd=None,
            table_class=None):
        if table_class is None:
            table_class = self.__class__
        if rnd is None:
            rnd = random.Random()

        table = table_class(header=self._header)
        data = []
        data.extend(self._data)
        data_len = len(data)

        for __ in xrange(sample_number):
            i = rnd.randrange(0, data_len)
            sample = data[i]
            table.add_record(sample)
            data.pop(i)
            data_len -= 1

        return table

    bootstrap = sample_with_replacement

    @classmethod
    def join_tables(cls, *args):
        table_class = cls
        if args:
            table = table_class(header=args[0].header)
            for arg in args:
                assert(args[0].header == arg.header)
                for record in arg:
                    table.add_record(record)
            return table
        else:
            return table_class()

    def __unicode__(self):
        return u'%s with %d elements' % (self.__class__.__name__, len(self.data))