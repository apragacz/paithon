class HashableSlice(object):

    def get_slice(self):
        return slice(self.start, self.stop, self.step)

    def __eq__(self, value):
        if value.__class__ not in [HashableSlice, slice]:
            return False
        if self.start != value.start:
            return False
        if self.stop != value.stop:
            return False
        if self.step != value.step:
            return False
        return True

    def __hash__(self):
        return hash(self.start) + hash(self.stop) + hash(self.step)

    def indices(self, value):
        s = self.get_slice().indices(value)
        return HashableSlice(s.start, s.stop, s.step)

    def __cmp__(self, value):
        if hasattr(value, 'get_slice'):
            value = value.get_slice()
        return cmp(self.get_slice(), value)


def sequence(x):
    if hasattr(x, '__len__'):
        return x
    else:
        return tuple(x)
