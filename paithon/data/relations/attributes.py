from abc import ABCMeta, abstractmethod, abstractproperty

from ...core.exceptions import ValidationError


class AbstractAttribute(object):

    __metaclass__ = ABCMeta

    def __init__(self, name):
        self._name = name
        self.initialize()

    def initialize(self):
        pass

    def load_values(self, values):
        pass

    def str_dump(self, value):
        return str(value)

    @abstractmethod
    def to_python(self, input_value):
        pass

    @abstractmethod
    def validate(self, value):
        pass

    @property
    def name(self):
        return self._name

    @abstractproperty
    def discrete(self):
        pass

    @abstractproperty
    def numeric(self):
        pass

    @abstractproperty
    def initialized(self):
        pass

    def __eq__(self, value):

        try:
            if self.__class__ != value.__class__:
                return False
            if self._name != value.name:
                return False
            return True
        except Exception:
            return False


class NominalAttribute(AbstractAttribute):

    def initialize(self):
        self._values = None

    def load_values(self, values):
        if not self._values:
            self._values = set(values)

    def to_python(self, input_value):
        return str(input_value)

    def validate(self, value):
        if not self._values or value not in self._values:
            raise ValidationError('%s not in %s' % (value, self._values))

    def __eq__(self, value):
        if not super(NominalAttribute, self).__eq__(value):
            return False
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

    def to_python(self, input_value):
        return str(input_value)

    def validate(self, value):
        pass

    @property
    def discrete(self):
        return False

    @property
    def numeric(self):
        return False

    @property
    def initialized(self):
        return True


class NumericAttribute(AbstractAttribute):

    def to_python(self, input_value):
        return float(input_value)

    def validate(self, value):
        try:
            float(value)
        except ValueError:
            raise ValidationError('%s is not a valid numeric' % (value))

    @property
    def discrete(self):
        return False

    @property
    def numeric(self):
        return True

    @property
    def initialized(self):
        return True


class IntegerAttribute(NumericAttribute):

    def to_python(self, input_value):
        return int(input_value)

    def validate(self, value):
        try:
            int(value)
        except ValueError:
            raise ValidationError('%s is not a valid integer' % (value))
