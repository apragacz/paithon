from paithon.utils.core import AbstractMethodError


import random
from collections import defaultdict


from datamining import vectors


class HeaderValidationError(Exception):
    pass


class Header(object):
    def __init__(self):
        self.columns_values = []

    def __eq__(self, value):
        try:
            return (self.columns_values == value.columns_values)
        except:
            return False

    def validate(self, record):
        if len(record) != len(self.columns_values):
            raise HeaderValidationError


class Table(object):
    def __init__(self, filename=None, header=None):
        self._data = []
        self._header = header if header is not None else Header()
        if filename:
            self.load(filename)

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        print key
        return self._data[key]

    def to_python(self, value):
        return str(value)

    def str_dump(self, value):
        return str(value)

    def set_header(self, header):
        self._header = header

    def add_record(self, record, overwrite_header=False):
        if overwrite_header:
            first_line = (len(self._data) == 0)
            if first_line:
                self._header._columns_values = [set() for _ in record]

            for i, item in enumerate(record):
                self._header._columns_values[i].add(item)

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

    def load(self, filename):
        self._data = []
        self._header = Header()
        with open(filename, 'rU') as f:
            for line in f:
                record = [self.to_python(item.strip())
                            for item in line.split(',')]

                self.add_record(record, overwrite_header=True)

    def save_arff(self, filename):
        with open(filename, 'w',) as f:
            x_len = len(self.data[0][0])
            y_len = len(self.data[0][1])
            f.write('@relation caravan\n')
            for i in range(x_len):
                f.write('@attribute A%d NUMERIC\n' % i)
            for i in range(y_len):
                attr_type = '{%s}' % (','.join(map(self.str_dump,
                                            self.header.y_columns_values[i])))
                f.write('@attribute class%d %s\n' % (i, attr_type))
            f.write('@data\n')
            for record in self.data:
                f.write(','.join(map(str, record[0])))
                f.write(',')
                f.write(','.join(map(str, record[1])))
                f.write('\n')

    def split_by_decision(self, decision_index=0, table_class=None):
        if table_class is None:
            table_class = self.__class__
        sp = defaultdict(lambda: table_class(header=self.header))

        for record in self.data:
            x, y = record
            sp[y[decision_index]].add_record(record)

        return sp

    def split_into_parts(self, part_number=10, table_class=None):
        if table_class is None:
            table_class = self.__class__
        parts = [table_class(header=self.header) for i in range(part_number)]

        for i, record in enumerate(self.data):
            parts[i % part_number].add_record(record)

        return parts

    def sample_with_replacement(self, sample_number, rnd=None, table_class=None):
        if table_class is None:
            table_class = self.__class__
        if rnd is None:
            rnd = random.Random()

        table = table_class(header=self.header)
        data_len = len(self.data)

        for __ in xrange(sample_number):
            table.add_record(self.data[rnd.randrange(0, data_len)])

        return table

    def sample_without_replacement(self, sample_number, rnd=None, table_class=None):
        if table_class is None:
            table_class = self.__class__
        if rnd is None:
            rnd = random.Random()

        table = table_class(header=self.header)
        data = []
        data.extend(self.data)
        data_len = len(data)

        for __ in xrange(sample_number):
            i = rnd.randrange(0, data_len)
            sample = data[i]
            table.add_record(sample)
            data.pop(i)
            data_len -= 1

        return table

    bootstrap = sample_with_replacement

    def process_x(self, x_transform):
        new_data = []
        for record in self.data:
            x, y = record
            new_record = (x_transform(x), y)
            #print new_record
            new_data.append(new_record)
        self.data = new_data
        self.reload_header()

    @property
    def x(self):
        return [x for x, __ in self.data]

    @property
    def y(self):
        return [y for __, y in self.data]

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

    def __repr__(self):
        return str(unicode(self))

    def __str__(self):
        return str(unicode(self))


class IntDecisionalTable(DecisionalTable):

    def to_python(self, value):
        return int(value)

    def str_dump(self, value):
        return str(value)

    @property
    def zero_x_vector(self):
        return vectors.zero(len(self.header.x_columns_values))

    @property
    def zero_y_vector(self):
        return vectors.zero(len(self.header.y_columns_values))

    @property
    def x_means(self):
        return vectors.avg(self.x)

    @property
    def x_variances(self):
        avg = vectors.avg(self.x)
        return vectors.avg([vectors.coord_sq(vectors.sub(x, avg)) for x in self.x])

    @property
    def x_stddevs(self):
        return vectors.coord_sqrt(self.x_variances)


class TableHeader(object):
    def __init__(self):
        self._d


class Table(object):
    def __init__(self, filename=None):
        self._data = []

    def add_record(self, record):
        self._data.append(record)

    def load(self, filename):
        raise AbstractMethodError()
