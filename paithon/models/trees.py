from abc import ABCMeta, abstractproperty

from .base import Model
from ..core.stat import collection


class DecisionTree(Model):
    def __init__(self, disortion_measure):
        self._root = None
        self._disortion_measure = disortion_measure

    def nominal_split(self, relation, attribute_index):
        decision_index = relation.decision_index
        dec_values = relation.attribute_values(decision_index)
        gain = self._disortion_measure(dec_values)
        sp = relation.split_by_attribute_values(attribute_index)
        for value, sub_relation in sp.iteritems():
            sub_dec_values = sub_relation.attribute_values(decision_index)
            gain -= self._disortion_measure(sub_dec_values)
        return (gain, sp, None)

    def numeric_split(self, relation, attribute_index, cut_value=None):
        if cut_value is None:
            values = set(relation.attribute_values(attribute_index))
        #TODO:

    def build_node_recursive(self, relation):
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
        self._lt_node = None
        self._split_value = None
        self._gte_node = None

    @property
    def children(self):
        result = []
        if self._lt_node:
            result.append(self._lt_node)
        if self._gte_node:
            result.append(self._gte_node)
        return result
