from paithon.core.exceptions import AbstractMethodError


class RecordWriter(object):

    def write_header(self, header):
        raise AbstractMethodError()

    def write_record(self, record):
        raise AbstractMethodError()

    def write_footer(self):
        raise AbstractMethodError()
