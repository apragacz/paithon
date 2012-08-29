import math
import random
from abc import abstractmethod

from .base import Model


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(x):
    return math.exp(-x) / (1.0 + math.exp(-x)) ** 2.0


class Percepton(Model):

    def __init__(self, num_of_inputs, rnd=None,
            threshold_function=None, threshold_derivative_function=None):
        self._last_output = None

        if not rnd:
            rnd = random.Random()

        if threshold_function:
            self._threshold_fun = threshold_function
        else:
            self._threshold_fun = sigmoid

        if threshold_derivative_function:
            self._threshold_derivative_fun = threshold_derivative_function
        else:
            self._threshold_derivative_fun = sigmoid_derivative

        self._weigths = []
        for _ in xrange(len(num_of_inputs)):
            self._weigths.append(rnd.uniform(0.0, 1.0))

    def output(self, inputs):
        self._last_output = self._threshold_fun(sum((w * x for w, x
                                                in zip(self._weigths, inputs))))
        return self._last_output


class PerceptonLayer(Model):

    def __init__(self, num_of_inputs, num_of_outputs, rnd=None,
            threshold_function=None, threshold_derivative_function=None):
        self._perceptons = []
        for _ in xrange(len(num_of_outputs)):
            self._perceptons.append(Percepton(num_of_inputs, rnd=rnd,
                    threshold_function=threshold_function,
                    threshold_derivative_function=threshold_derivative_function))

    def outputs(self, inputs):
        return [p.output(inputs) for p in self._perceptons]


class PerceptonNetwork(Model):

    @abstractmethod
    def outputs(self, inputs):
        pass


class PerceptonLayeredNetwork(PerceptonNetwork):
    def __init__(self, num_of_inputs, num_of_outputs,
            num_of_immediate_elements_list=[], rnd=None,
            threshold_function=None, threshold_derivative_function=None):
        self._layers = []
        for num_of_immediate_elems in num_of_immediate_elements_list:
            self._layers.append(PerceptonLayer(num_of_inputs,
                    num_of_immediate_elems,
                    rnd=rnd, threshold_function=threshold_function,
                    threshold_derivative_function=threshold_derivative_function))
            num_of_inputs = num_of_immediate_elems

        self._layers.append(PerceptonLayer(num_of_inputs, num_of_outputs,
                rnd=rnd, threshold_function=threshold_function,
                threshold_derivative_function=threshold_derivative_function))

    def outputs(self, inputs):
        return self.feed_forward(inputs)

    def feed_forward(self, inputs):
        values = inputs
        for layer in self._layers:
            values = layer.outputs(values)
        return values
