'''
The vector (linear space element) abstraction
'''


class Vector(tuple):

    def __add__(self, other):
        return Vector((e1 + e2 for e1, e2 in zip(self, other)))

    def __sub__(self, other):
        return Vector((e1 - e2 for e1, e2 in zip(self, other)))

    def __mul__(self, other):
        return Vector((e1 * e2 for e1, e2 in zip(self, other)))

    def __div__(self, other):
        return Vector((e1 / e2 for e1, e2 in zip(self, other)))

    def __floordiv__(self, other):
        return Vector((e1 // e2 for e1, e2 in zip(self, other)))

    def __abs__(self):
        if len(self) > 0:
            return reduce(lambda acc, x: max(abs(x), acc), self, abs(self[0]))
        else:
            return 0.0

    def __pow__(self, other, modulo):
        return Vector((pow(e, other, modulo) for e in self))

    def __neg__(self):
        return Vector((-e1 for e1 in self))

    def __pos__(self):
        return self

    def __addi__(self, other):
        self = self + other
        return self

    def __muli__(self, other):
        self = self * other
        return self

    def __subi__(self, other):
        self = self - other
        return self

    def __divi__(self, other):
        self = self / other
        return self

    def __floordivi__(self, other):
        self = self // other
        return self

    def abs(self):
        return Vector((abs(e) for e in self))


class SparseVector(object):
    def __init(self, input=None, sparse_input=None, default_value=0.0, length=None):
        self._default_value = default_value
        if input is not None:
            if isinstance(input, SparseVector):
                self._data = {}
                self._data.update(input._data)
                self._length = input._length
            else:
                self._data = dict(enumerate(input))
        elif sparse_input is not None:
            self._data = dict(sparse_input)
        if length is not None:
            self._length = length
        else:
            self._length = max(self._data.keys())

    def __len__(self):
        return self._length

    def __getitem__(self, key):
        return self._data.get(key, self._default_value)

    def _create_from_two(self, other, fun):
        keys = set(self._data.keys() + other._data.keys())
        sparse_input = ((k, fun(self[k], other[k])) for k in keys)
        default_value = fun(self._default_value, other._default_value)
        length = max([len(self), len(other)])
        return SparseVector(sparse_input=sparse_input,
                            default_value=default_value,
                            length=length)

    def _create_from_one(self, fun):
        sparse_input = ((k, fun(v)) for k, v in self._data.iteritems())
        default_value = fun(self._default_value)
        length = len(self)
        return SparseVector(sparse_input=sparse_input,
                            default_value=default_value,
                            length=length)

    def __add__(self, other):
        return self._create_from_two(other, lambda e1, e2: e1 + e2)

    def __sub__(self, other):
        return self._create_from_two(other, lambda e1, e2: e1 - e2)

    def __mul__(self, other):
        return self._create_from_two(other, lambda e1, e2: e1 * e2)

    def __div__(self, other):
        return self._create_from_two(other, lambda e1, e2: e1 / e2)

    def __floordiv__(self, other):
        return self._create_from_two(other, lambda e1, e2: e1 // e2)

    def __pow__(self, other, modulo):
        return self._create_from_one(lambda e: pow(e, other, modulo))
