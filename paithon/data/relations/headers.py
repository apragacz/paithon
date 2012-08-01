from paithon.core.exceptions import AbstractMethodError, ValidationError


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
    def name(self):
        return self._name

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
        if not self._values:
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
    def initialized(self):
        return bool(self._values)

    @property
    def values(self):
        return self._values if self._values else set()


class StringAttribute(AbstractAttribute):
    def initialize(self):
        pass

    def to_python(self, input_value):
        return str(input_value)

    @property
    def discrete(self):
        return False

    @property
    def numeric(self):
        return False

    @property
    def initialized(self):
        return True

    def __eq__(self, value):
        if not isinstance(value, StringAttribute):
            return False
        if self._name != value.name:
            return False
        return True


class NumericAttribute(AbstractAttribute):
    def initialize(self):
        pass

    def to_python(self, input_value):
        return float(input_value)

    @property
    def discrete(self):
        return False

    @property
    def numeric(self):
        return True

    @property
    def initialized(self):
        return True

    def __eq__(self, value):
        if not isinstance(value, NumericAttribute):
            return False
        if self._name != value.name:
            return False
        return True


class IntegerAttribute(NumericAttribute):
    def to_python(self, input_value):
        return int(input_value)


class Header(object):
    def __init__(self, attributes=None, record_len=0,
                    constructor=lambda name: StringAttribute(name)):
        if attributes:
            self._attributes = attributes
        else:
            self._attributes = [constructor('A%d' % (i + 1))
                                for i in range(record_len)]
        self._decision_index = None

    def set_decision_index(self, index):
        self._decision_index = index

    @property
    def attributes(self):
        return self._attributes

    def validate(self, record):
        if len(record) != len(self._attributes):
            raise HeaderValidationError('invalid record length')

    def to_python_by_index(self, index, value):
        return self._attributes[index].to_python(value)

    def __eq__(self, value):
        if not isinstance(value, Header):
            return False
        if not hasattr(value, '_attributes'):
            return False
        if not hasattr(value, '_decision_index'):
            return False
        if self._attributes != value._attributes:
            return False
        if self._decision_index != value._decision_index:
            return False
        return True

    def __len__(self):
        return len(self._attributes)

    def __iter__(self):
        return iter(self._attributes)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__class__(attributes=self._attributes[key])
        return self._attributes[key]
