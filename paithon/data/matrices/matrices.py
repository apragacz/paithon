

class SparseRow(object):
    def __init__(self, default_value=None):
        self._data = {}
        self._default = default_value

    def _getitem__(self, key):
        self._data.get(key, self._default)

    def _setitem_(self, key, value):
        if value == self._default:
            if key in self._data:
                del self._data[key]
        else:
            self._data[key] = value


class SparseMatrix(object):
    def __init__(self, default_value=None):
        self._data = {}
        self._default = default_value

    def _getitem__(self, key):
        if isinstance(key, tuple) and len(key) == 2:
            x, y = key
            return self[x][y]
        else:
            self._data.setdefault(key, SparseRow(default_value=self._default))
            return self._data[key]
