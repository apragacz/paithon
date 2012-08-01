from paithon.core.exceptions import AbstractMethodError
from paithon.data.relations.readers.base import RecordReader
from paithon.data.relations.headers import (Header, NumericAttribute,
    NominalAttribute)


class AbstractRecordCSVReader(RecordReader):

    def __init__(self, in_file, header=False, separator=','):
        self._header = None
        self._header_present = header
        self._record_cache = None
        self._f = in_file
        self._sep = separator

    def attribute(self, index, name):
        raise AbstractMethodError()

    def read_header(self):
        if self._header_present:
            line = self._f.readline()
            assert(line)
            header_record = [item.strip() for item in line.split(self._sep)]
            attributes = [self.attribute(i, name)
                                for i, name in enumerate(header_record)]
        else:
            assert(self._record_cache is None)
            self._record_cache = self.read_record_core()
            header_len = len(self._record_cache) if self._record_cache else 0
            attributes = [self.attribute(i, None)
                                for i in range(header_len)]
        self._header = Header(attributes=attributes)
        return self._header

    def read_record_core(self):
        line = self._f.readline()
        if not line:
            return None
        record_elems = [self.to_python(item.strip(), i)
                    for i, item in enumerate(line.split(self._sep))]
        return tuple(record_elems)

    def read_record(self):
        if self._record_cache is not None:
            record = self._record_cache
            self._record_cache = None
            return record
        else:
            return self.read_record_core()

    def to_python(self, value, index):
        return self._header.to_python_by_index(index, value)

    def __iter__(self):
        return self

    def next(self):
        record = self.read_record()
        if record is None:
            raise StopIteration()
        return record

    def __del__(self):
        pass
        #self._f.close()


class RecordNumericCSVReader(AbstractRecordCSVReader):

    def attribute(self, index, name):
        return NumericAttribute(name)


class RecordNominalCSVReader(AbstractRecordCSVReader):

    def attribute(self, index, name):
        return NominalAttribute(name)
