from paithon.core.exceptions import ValidationError
from paithon.data.relations.attributes import StringAttribute


class HeaderValidationError(ValidationError):
    pass


class Header(object):
    def __init__(self, attributes=None, decision_index=None, record_len=0,
                    constructor=lambda name: StringAttribute(name)):
        if attributes is not None:
            self._attributes = attributes
        else:
            self._attributes = [constructor('A%d' % (i + 1))
                                for i in range(record_len)]
        self._decision_index = decision_index

    def set_decision_index(self, index):
        if index is None or not self._attributes:
            self._decision_index = None
        else:
            self._decision_index = index % len(self._attributes)

    def get_decision_index(self):
        return self._decision_index

    def validate(self, record):
        if len(record) != len(self._attributes):
            raise HeaderValidationError('invalid record length')

    def split_record_by_decision(self, record):
        x = []
        y = None
        for i, value in enumerate(record):
            if i == self._decision_index:
                y = value
            else:
                x.append(value)
        return (tuple(x), y)

    @property
    def attributes(self):
        return self._attributes

    decision_index = property(set_decision_index, get_decision_index)

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
