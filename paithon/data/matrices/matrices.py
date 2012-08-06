

class SparseMatrix(object):
    def __init__(self, default_value=None):
        self._data = {}
        self._default = default
