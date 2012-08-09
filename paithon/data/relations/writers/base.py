from abc import ABCMeta, abstractmethod


class RecordWriter(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def write_header(self, header):
        pass

    @abstractmethod
    def write_record(self, record):
        pass

    @abstractmethod
    def write_footer(self):
        pass
