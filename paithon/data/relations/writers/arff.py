from paithon.data.relations.headers import Header
from paithon.data.relations.writers.core import RecordWriter


class RecordARFFWriter(RecordWriter):

    def __init__(self, out_file):
        self._f = out_file
        self._header = Header()

    def str_dump(self, value, index):
        #use attribute info in the future
        return str(value)

    def write_header(self, header):
        self._header = header
        self._f.write('@relation unnamed\n')
        for attribute in header.attributes:
            if attribute.numeric:
                type_str = 'NUMERIC'
            elif attribute.discrete:
                dump = lambda ((i, v)): self.str_dump(v, i)
                type_str = '{%s}' % (','.join(map(dump,
                                                enumerate(attribute.values))))
            else:
                type_str = 'STRING'
            self._f.write('@attribute %s %s\n' % (attribute.name, type_str))
        self._f.write('@data\n')

    def write_record(self, record):
        dump = lambda ((i, v)): self.str_dump(v, i)
        self._f.write(','.join(map(dump, enumerate(record))))
        self._f.write('\n')

    def write_footer(self):
        self._f.flush()

    def close(self):
        self._f.close()

    def __del__(self):
        pass
        #self._f.close()
