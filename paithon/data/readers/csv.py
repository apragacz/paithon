from paithon.utils.core import AbstractMethodError
from paihton.data.readers.core import RecordReader
from paihton.data.tables.core import Header


class AbstractRecordCSVReader(RecordReader):

    def column_info(self, index):
        raise AbstractMethodError()

    def __init__(self, filename):
        self._header = None
        self._record_cache = None
        self._filename = filename
        self._f = open(filename, 'rU')

    def read_header(self):
        if self._header is None:
            if self._record_cache is None:
                self._record_cache = self.read_record_core()
            if self._record_cache is None:
                column_infos = []
            else:
                column_infos = [self.column_info(i)
                                for i in range(len(self._record_cache))]
            self._header = Header(column_infos=column_infos)

        return self._header

    def read_record_core(self):
        line = self._f.readline()
        if not line:
            return None
        record = [self.to_python(item.strip(), i)
                    for i, item in enumerate(line.split(','))]
        return record

    def read_record(self):
        if self._record_cache is not None:
            record = self._record_cache
            self._record_cache = None
            return record
        else:
            return self.read_record_core()

    def to_python(self, value, index):
        return str(value)

    def __iter__(self):
        return self

    def __next__(self):
        record = self.read_record()
        if record is None:
            raise StopIteration()

    def __del__(self):
        self._f.close()


class RecordCSVReader(AbstractRecordCSVReader):
    def __init__(self, filename, default_type):
        super(RecordCSVReader, self).__init__(filename)

    def column_info(self, index):
        raise AbstractMethodError()
