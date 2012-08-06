from paithon.core.exceptions import AbstractMethodError
from paithon.data.relations.readers.base import RecordReader
from paithon.data.relations.headers import (Header, NumericAttribute,
    NominalAttribute)


class AbstractRecordCSVReader(RecordReader):

    def __init__(self, in_file, header=False, separator=',', quote='"'):
        self._header = None
        self._header_present = header
        self._record_cache = None
        self._f = in_file
        self._sep = separator
        self._quote = quote

    def attribute(self, index, name, value):
        return AbstractMethodError()

    def read_header(self):
        assert(self._record_cache is None)
        if self._header_present:
            line = self._f.readline()
            assert(line)
            header_names = [item.strip() for item in line.split(self._sep)]
            first_record = self.read_record_core()
            assert(first_record)
            assert(len(first_record) == len(header_names))
            self._record_cache = first_record
            attributes = [self.attribute(i, name, value)
                            for i, (name, value) in enumerate(zip(header_names,
                                                                first_record))]
        else:
            first_record = self.read_record_core()
            self._record_cache = first_record
            first_record = first_record or []
            attributes = [self.attribute(i, None, value)
                                for i, value in  enumerate(first_record)]
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
        return self._header.attributes[index].to_python(value)

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

    def attribute(self, index, name, value):
        return NumericAttribute(name)


class RecordNominalCSVReader(AbstractRecordCSVReader):

    def attribute(self, index, name, value):
        return NominalAttribute(name)


class SmartCSVReader(AbstractRecordCSVReader):

    def attribute(self, index, name, value):
        return NumericAttribute(name)
