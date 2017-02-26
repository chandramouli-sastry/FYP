from __future__ import division
import types
import math



class Properties:

    def __init__(self,list_values):
        functions = []
        for i in self.__dict__:
            if type(i) == types.FunctionType:
                functions.append(i)
        properties = []
        for func in functions:
            properties.append(self.__dict__[func](list_values))
        self.property = self.norm(properties)

    def norm(self,properties):
        return (sum(map(lambda x:x**2, properties))) ** 0.5

    def _compute_mean(self,list_values):
        return sum(list_values)/float(len(list_values))

    def compute_entropy(self,list_values):
        sum_array = sum(list_values)
        result = sum([i / sum_array * math.log(i / sum_array) for i in list_values])
        return result

    def compute_variance(self,list_values):
        mean = self._compute_mean(list_values)
        summ = 0
        for i in list_values:
            summ += (i-mean)**2
        return summ/float(len(list_values))

    def compute_lorenz_measure(self,list_values):
        #TODO : Implement lorenz measure for list of values.
        measure = 0
        return measure