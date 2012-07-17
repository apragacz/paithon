from paithon.data.tables.core import TYPE_NOMINAL, TYPE_NUMERIC
from paithon.data.writers.core import RecordWriter


class RecordARFFWriter(RecordWriter):

    def __init__(self, filename):
        self._filename = filename
        self._f = open(filename, 'w')

    def str_dump(self, value, index):
        return str(value)

    def write_header(self, header):
        self._f.write('@relation unnamed\n')
        for info in header.column_infos:
            if info.column_type == TYPE_NUMERIC:
                type_str = 'NUMERIC'
            elif info.column_type == TYPE_NOMINAL:
                dump = lambda ((i, v)): self.str_dump(v, i)
                type_str = '{%s}' % (','.join(map(dump,
                                                    enumerate(info.values))))
            self._f.write('@attribute %s %s\n' % (info.name, type_str))
        self._f.write('@data\n')

    def write_record(self, record):
        self._f.write(','.join(map(str, record)))
        self._f.write('\n')

    def close(self):
        self._f.close()

    def __del__(self):
        self._f.close()
