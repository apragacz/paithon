from abc import ABCMeta, abstractproperty

from .base import Model
from ..core.stat import collection


class HashableSlice(slice):

    def __hash__(self):
        return hash(self.start) + hash(self.stop) + hash(self.step)


class DecisionTree(Model):
    def __init__(self, disortion_measure):
        self._root = None
        self._disortion_measure = disortion_measure

    def gain(self, all_dec_values, dec_values_split):
        gain = self._disortion_measure(all_dec_values)
        for dec_values in  dec_values_split:
            gain -= self._disortion_measure(dec_values)
        return gain

    def value_split_dict(self, cond_dec_records, cond_attribute_index):
        sp_dict = {}
        for pair in cond_dec_records:
            cond_record, _ = pair
            cond_value = cond_record[cond_attribute_index]
            sp_dict.setdefault(cond_value, []).append(pair)
        return sp_dict

    def cut_split_dict(self, cond_dec_records, cond_attribute_index,
                        cut_value):

        lt_records = []
        gte_records = []
        for pair in cond_dec_records:
            cond_record, _ = pair
            cond_value = cond_record[cond_attribute_index]
            if cond_value < cut_value:
                lt_records.append(pair)
            else:
                gte_records.append(pair)
        sp_dict = {
            HashableSlice(None, cut_value): lt_records,
            HashableSlice(cut_value, None): gte_records,
        }
        return sp_dict

    def iter_decisions(self, cond_dec_records):
        for cond_rec, dec_rec in cond_dec_records:
            yield dec_rec[0]

    def iter_conditional_values(self, cond_dec_records, index):
        for cond_record, _ in cond_dec_records:
            yield cond_record[index]

    def score(self, cond_dec_records, split_dict):
        all_dec_values = list(self.iter_decisions(cond_dec_records))
        dec_values_split = [self.iter_decisions(x) for x in split_dict.values()]
        score_fun = self.gain
        return score_fun(all_dec_values, dec_values_split)

    def find_best_split_dict(self, cond_dec_records, cond_attributes):

        assert(hasattr(cond_attributes, '__len__'))
        assert(filter(None, cond_attributes))

        def generate_splits():
            for i, cond_attr in enumerate(cond_attributes):
                if cond_attr is not None:
                    if cond_attr.discrete:
                        spd = self.value_split_dict(cond_dec_records, i)
                        score = self.score(cond_dec_records, spd)
                        yield (score, spd, i)
                    elif cond_attr.numeric:
                        cond_values = set(self.iter_conditional_values(
                                            cond_dec_records, i))
                        for cond_value in cond_values:
                            spd = self.cut_split_dict(cond_dec_records, i,
                                                        cond_value)
                            score = self.score(cond_dec_records, spd)
                            yield (score, spd, i)

        return max(generate_splits(), key=lambda x: x[0])[1:2]

    def build_node_recursive(self, cond_dec_records, cond_attributes):
        (spd, i) = self.find_best_split_dict(cond_dec_records, cond_attributes)
        if (len(spd) == 2 and isinstance(spd.keys()[0], slice)
                and isinstance(spd.keys()[1], slice)):
            #cut split
            slice1, slice2 = spd.keys()
            cut_value = None
            gte_split = None
            lt_split = None
            if slice1.start is not None:
                cut_value = slice1.start
                lt_split = spd[slice2]
                gte_split = spd[slice1]
            else:
                cut_value = slice1.stop
                lt_split = spd[slice1]
                gte_split = spd[slice2]

            node = InequalityDecisionNode()
            node._cut_value = cut_value
            node._lt_node = self.build_node_recursive(lt_split,
                                                        cond_attributes)
            node._gte_node = self.build_node_recursive(gte_split,
                                                        cond_attributes)
            return node

        else:
            cond_dec_records_copy = cond_dec_records[:]
            cond_dec_records_copy[i] = None
            node = EqualityDecisionNode()
            node._node_map = {}
            for value, value_split in spd.iteritems():
                node._node_map[value] = self.build_node_recursive(value_split,
                                                        cond_dec_records_copy)



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
