from paithon.core.exceptions import AbstractMethodError
from paihton.data.tables.readers.core import RecordReader
from paihton.data.tables.headers import (Header, NumericColumnInfo,
    NominalColumnInfo)


class AbstractRecordCSVReader(RecordReader):

    def __init__(self, in_file, header=False, separator=','):
        self._header = None
        self._header_present = header
        self._record_cache = None
        self._f = in_file
        self._sep = separator

    def column_info(self, index, name):
        raise AbstractMethodError()

    def read_header(self):
        if self._header_present:
            line = self._f.readline()
            assert(line)
            header_record = [item.strip() for item in line.split(self._sep)]
            column_infos = [self.column_info(i, name)
                                for i, name in enumerate(header_record)]
        else:
            assert(self._record_cache is None)
            self._record_cache = self.read_record_core()
            header_len = len(self._record_cache) if self._record_cache else 0
            column_infos = [self.column_info(i, None)
                                for i in range(header_len)]
        self._header = Header(column_infos=column_infos)
        return self._header

    def read_record_core(self):
        line = self._f.readline()
        if not line:
            return None
        record = [self.to_python(item.strip(), i)
                    for i, item in enumerate(line.split(self._sep))]
        return record

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

    def __next__(self):
        record = self.read_record()
        if record is None:
            raise StopIteration()
        return record

    def __del__(self):
        pass
        #self._f.close()


class RecordNumericCSVReader(AbstractRecordCSVReader):

    def column_info(self, index, name):
        return NumericColumnInfo(name)


class RecordNominalCSVReader(AbstractRecordCSVReader):

    def column_info(self, index, name):
        return NominalColumnInfo(name)
