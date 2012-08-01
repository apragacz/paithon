from paithon.core.exceptions import AbstractMethodError, ValidationError
from paithon.core.stat import mean_and_variance


class HeaderValidationError(ValidationError):
    pass


class AbstractAttribute(object):
    def __init__(self, name):
        self._name = name
        self.initialize()

    def initialize(self):
        raise AbstractMethodError()

    def load_values(self, values):
        raise AbstractMethodError()

    def validate(self, value):
        raise AbstractMethodError()

    @property
    def discrete(self):
        raise AbstractMethodError()

    @property
    def numeric(self):
        raise AbstractMethodError()

    @property
    def initialized(self):
        raise AbstractMethodError()


class NominalAttribute(AbstractAttribute):
    def initialize(self):
        self._values = None

    def load_values(self, values):
        self._values = set(values)

    def to_python(self, input_value):
        return str(input_value)

    def __eq__(self, value):
        if hasattr(value, '_values'):
            return (self._values == value._values)
        return False

    @property
    def discrete(self):
        return True

    @property
    def numeric(self):
        return False

    @property
    def values(self):
        return self._values

    @property
    def initialized(self):
        return bool(self._values)


class StringColumnInfo(AbstractColumnInfo):
    def initialize(self):
        self._values_lengths = {}

    def load_values(self, values):
        for value in values:
            k = len(value)
            self._values_lengths[k] = self._values_lengths.setdefault(k, 0) + 1

    def to_python(self, input_value):
        return str(input_value)

    def __eq__(self, value):
        if hasattr(value, '_values_lengths'):
            return (self._values_lengths == value._values_lengths)
        return False

    @property
    def column_type(self):
        return COLUMN_TYPE_STRING

    @property
    def discrete(self):
        return False

    @property
    def numeric(self):
        return False


class NumericColumnInfo(AbstractColumnInfo):
    def initialize(self):
        self._mean = None
        self._variance = None

    def load_values(self, values):
        self._mean, self._variance = mean_and_variance(values)

    def to_python(self, input_value):
        return float(input_value)

    def __eq__(self, value):
        if hasattr(value, '_mean') and hasattr(value, '_variance'):
            return (self._mean == value._mean
                        and self._variance == value._variance)
        return False

    @property
    def column_type(self):
        return COLUMN_TYPE_NUMERIC

    @property
    def discrete(self):
        return False

    @property
    def numeric(self):
        return True


class IntegerColumnInfo(NumericColumnInfo):
    def to_python(self, input_value):
        return int(input_value)


class Header(object):
    def __init__(self, column_infos=None, record_len=0,
                    constructor=lambda name: StringColumnInfo(name)):
        if column_infos:
            self._column_infos = column_infos
        else:
            self._column_infos = [constructor('A%d' % (i + 1))
                                for i in range(record_len)]

    def __eq__(self, value):
        if hasattr(value, '_column_infos'):
            return (self._column_infos == value._column_infos)
        return False

    @property
    def column_infos(self):
        return self._column_infos

    def load_values_by_index(self, index, values):
        self._column_infos[index].load_values(values)

    def validate(self, record):
        if len(record) != len(self._column_infos):
            raise HeaderValidationError('invalid record length')

    def to_python_by_index(self, index, value):
        return self._column_infos[index].to_python(value)

    def __len__(self):
        return len(self._column_infos)
