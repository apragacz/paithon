from paithon.core.exceptions import AbstractMethodError, ValidationError

from ...relations.attributes import (NumericAttribute,
    NominalAttribute)
from ...relations.headers import Header

from .base import RecordReader


class AbstractRecordCSVReader(RecordReader):

    def __init__(self, in_file, header=False, separator=',', quote='"'):
        self._header = None
        self._header_present = header
        self._record_buffer = []
        self._f = in_file
        self._sep = separator
        self._quote = quote

    def attribute(self, index, name, info):
        return AbstractMethodError()

    def raw_row_elements(self, line):
        #TODO: more complicated cases
        raw_row_elems = [elem for elem in line.rstrip().split(self._sep)]
        return raw_row_elems

    def row_elements(self, line):
        #TODO: more complicated cases
        row_elems = [elem.strip(self._quote)
                            for elem in self.raw_row_elements(line)]
        return row_elems

    def row_element_infos(self, line):
        def get_info(raw_elem):
            info = {}
            info['type'] = 'string'
            info['quoted'] = False
            if (raw_elem.startswith(self._quote)
                    and raw_elem.endswith(self._quote)):
                info['type'] = 'string'
                info['quoted'] = True
                return info
            try:
                int(raw_elem)
                info['type'] = 'integer'
                return info
            except ValueError:
                pass
            try:
                float(raw_elem)
                info['type'] = 'numeric'
                return info
            except ValueError:
                pass
            return info
        raw_row_elems = self.raw_row_elements(line)
        return [get_info(raw_elem) for raw_elem in raw_row_elems]

    def read_header(self):
        assert(not self._record_buffer)
        header_names = []
        if self._header_present:
            line = self._f.readline()
            if not line:
                raise ValidationError('No header line')
            header_names = self.row_elements(line)

        line = self._f.readline()
        if line:
            row_elems = self.row_elements(line)
            row_elem_infos = self.row_element_infos(line)
            if not self._header_present:
                header_names = [None] * len(row_elems)
            assert(len(row_elems) == len(header_names))
            assert(len(row_elem_infos) == len(header_names))
        else:
            row_elem_infos = [{} for _ in range(len(header_names))]

        attributes = [self.attribute(i, name, info)
                        for i, (name, info) in enumerate(zip(header_names,
                                                            row_elem_infos))]
        self._header = Header(attributes=attributes)
        if line:
            self._record_buffer.append(self.record_from_row_elements(row_elems))

        return self._header

    def record_from_row_elements(self, row_elems):
        record_elems = [self.to_python(elem, i)
                        for i, elem in enumerate(row_elems)]
        return tuple(record_elems)

    def read_record_core(self):
        line = self._f.readline()
        if not line:
            return None
        row_elems = self.row_elements(line)
        return self.record_from_row_elements(row_elems)

    def read_record(self):
        if self._record_buffer:
            record = self._record_buffer.pop(0)
            return record
        else:
            record = self.read_record_core()
            return record

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

    def attribute(self, index, name, info):
        return NumericAttribute(name)


class RecordNominalCSVReader(AbstractRecordCSVReader):

    def attribute(self, index, name, info):
        return NominalAttribute(name)


class SmartCSVReader(AbstractRecordCSVReader):

    def attribute(self, index, name, info):
        info_type = info.get('type', 'undefined')
        type_cls_map = {
            'integer': NumericAttribute,
            'string': NominalAttribute,
            'numeric': NumericAttribute,
        }
        cls = type_cls_map.get(info_type, NominalAttribute)
        return cls(name)
