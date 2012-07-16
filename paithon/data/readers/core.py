from paithon.utils.core import AbstractMethodError


class RecordReader(object):

    def read_record(self):
        raise AbstractMethodError()
