from abc import ABCMeta, abstractproperty

from .base import Model
from ..core.stat import collection


class DecisionTree(Model):
    def __init__(self, disortion_measure):
        self._root = None
        self._disortion_measure = disortion_measure

    def gain(self, all_values, values_split):
        gain = self._disortion_measure(all_values)
        for values in  values_split:
            gain -= self._disortion_measure(values)
        return gain

    def value_split(self, cond_dec_records, cond_attribute_index):
        sp_dict = {}
        for cond_rec, dec_rec in cond_dec_records:
            cond_value = cond_rec[cond_attribute_index]
            dec_value = dec_rec[0]
            sp_dict.setdefault(cond_value, []).append(dec_value)
        return sp_dict.values()

    def cut_split(self, cond_dec_records, cond_attribute_index, cut_value):
        lt_values = []
        gte_values = []
        for cond_rec, dec_rec in cond_dec_records:
            cond_value = cond_rec[cond_attribute_index]
            dec_value = dec_rec[0]
            if cond_value < cut_value:
                lt_values.append(dec_value)
            else:
                gte_values.append(dec_value)
        return [lt_values, gte_values]

    def build_node_recursive(self, cond_dec_records):
        pass


class DecisionNode(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        self._attribute = None
        self._attribute_index = None

    @abstractproperty
    def children(self):
        pass


class EqualityDecisionNode(DecisionNode):

    def __init__(self):
        super(EqualityDecisionNode, self).__init__()
        self._node_map = {}

    @property
    def children(self):
        return self._node_map.values()


class InequalityDecisionNode(DecisionNode):

    def __init__(self):
        super(InequalityDecisionNode, self).__init__()
        self._cut_value = None
        self._lt_node = None
        self._gte_node = None

    @property
    def children(self):
        result = []
        if self._lt_node:
            result.append(self._lt_node)
        if self._gte_node:
            result.append(self._gte_node)
        return result
