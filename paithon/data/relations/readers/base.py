from abc import ABCMeta, abstractmethod


class RecordReader(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def read_header(self):
        pass

    @abstractmethod
    def read_record(self):
        pass
