from paithon.core.exceptions import AbstractMethodError


class RecordReader(object):

    def read_header(self):
        raise AbstractMethodError()

    def read_record(self):
        raise AbstractMethodError()
