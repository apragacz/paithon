import random
from paithon.data.relations.headers import Header


class Relation(object):
    def __init__(self, data=None, header=None):
        self._data = data if data else []
        self._header = header if header is not None else Header()

    def set_decision_index(self, index):
        self._header.set_decision_index(index)

    def add_record(self, record):
        self._data.append(record)

    def read(self, reader):
        self._data = []
        self._header = reader.read_header()
        for record in reader:
            self.add_record(record)

        for index, attribute in enumerate(self._header):
            if not attribute.initialized:
                attribute.load_values(self.attribute_values(index))

    def write(self, writer):
        writer.write_header(self._header)
        for record in self._data:
            writer.write_record(record)
        writer.write_footer()

    def iter_attribute_values(self, attribute_index):
        for record in self._data:
            yield record[attribute_index]

    def attribute_values(self, attribute_index):
        return list(self.iter_attribute_values(attribute_index))

    def split_by_column_values(self, attribute_index):
        cls = self.__class__
        sp = {}

        for record in self._data:
            value = record[attribute_index]
            if value not in sp:
                sp[value] = cls(header=self._header)
            sp[value].add_record(record)

        return sp

    def split_into_parts(self, part_number=10, table_class=None):
        if table_class is None:
            table_class = self.__class__
        parts = [table_class(header=self._header) for i in range(part_number)]

        for i, record in enumerate(self._data):
            parts[i % part_number].add_record(record)

        return parts

    def sample_with_replacement(self, sample_number, rnd=None):
        relation_cls = self.__class__
        if rnd is None:
            rnd = random.Random()

        table = relation_cls(header=self._header)
        data_len = len(self._data)

        for __ in xrange(sample_number):
            table.add_record(self._data[rnd.randrange(0, data_len)])

        return table

    def sample_without_replacement(self, sample_number, rnd=None):
        relation_cls = self.__class__
        if rnd is None:
            rnd = random.Random()

        table = relation_cls(header=self._header)
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

    @property
    def attributes(self):
        return self._header.attributes

    @property
    def conditional_part(self):
        i = self._header.get_decision_index()
        if i is None:
            conditional_data = self._data
            header = self._header
        else:
            attributes = self._header.attributes
            conditional_atributes = attributes[:i] + attributes[(i + 1):]
            conditional_data = [record[:i] + record[(i + 1):]
                                for record in self._data]
            header = Header(attributes=conditional_atributes)
        return self.__class__(data=conditional_data, header=header)

    @property
    def decisional_part(self):
        i = self._header.get_decision_index()
        if i is None:
            decisional_data = [() for _ in xrange(len())]
            header = Header(attributes=[])
        else:
            decisional_attributes = [self._header.attributes[i]]
            decisional_data = [(record[i],) for record in self._data]
            header = Header(attributes=decisional_attributes, decision_index=0)
        return self.__class__(data=decisional_data, header=header)

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__class__(data=self._data[key], header=self._header)
        else:
            return self._data[key]

    @classmethod
    def join_tables(cls, *args):
        relation_cls = cls
        if args:
            relation = relation_cls(header=args[0].header)
            for arg in args:
                assert(args[0].header == arg.header)
                for record in arg:
                    relation.add_record(record)
            return relation
        else:
            return relation_cls()

    def __unicode__(self):
        return u'%s with %d elements' % (self.__class__.__name__, len(self.data))
