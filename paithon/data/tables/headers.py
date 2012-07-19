from paithon.core.exceptions import AbstractMethodError, ValidationError
from paithon.utils.stat import mean_and_variance


class HeaderValidationError(ValidationError):
    pass


COLUMN_TYPE_NOMINAL = 1
COLUMN_TYPE_NUMERIC = 2
COLUMN_TYPE_STRING = 3


class AbstractColumnInfo(object):
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
    def column_type(self):
        raise AbstractMethodError()

    @property
    def is_discrete(self):
        raise AbstractMethodError()

    @property
    def is_numeric(self):
        raise AbstractMethodError()


class NominalColumnInfo(AbstractColumnInfo):
    def initialize(self):
        self._values = set()

    def load_values(self, values):
        self._values = set(values)

    def __eq__(self, value):
        if hasattr(value, '_values'):
            return (self._values == value._values)
        return False

    @property
    def column_type(self):
        return COLUMN_TYPE_NOMINAL

    @property
    def is_discrete(self):
        return True

    @property
    def is_numeric(self):
        return False


class StringColumnInfo(AbstractColumnInfo):
    def initialize(self):
        pass

    def load_values(self, values):
        self._values = set(values)

    def __eq__(self, value):
        if hasattr(value, '_values'):
            return (self._values == value._values)
        return False

    @property
    def column_type(self):
        return COLUMN_TYPE_NOMINAL

    @property
    def is_discrete(self):
        return False

    @property
    def is_numeric(self):
        return False


class NumericColumnInfo(AbstractColumnInfo):
    def initialize(self):
        self._mean = None
        self._variance = None

    def load_values(self, values):
        self._mean, self._variance = mean_and_variance(values)

    def __eq__(self, value):
        if hasattr(value, '_mean') and hasattr(value, '_variance'):
            return (self._mean == value._mean
                        and self._variance == value._variance)
        return False

    @property
    def column_type(self):
        return COLUMN_TYPE_NUMERIC

    @property
    def is_discrete(self):
        return False

    @property
    def is_numeric(self):
        return True
