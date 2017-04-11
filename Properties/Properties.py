
import types
import math
from collections import Counter


class Properties:

    def __init__(self,list_values,discrete = True,ordering = False):
        functions = []
        self.discrete = discrete
        for i in Properties.__dict__:
            if type(Properties.__dict__[i]) == types.FunctionType and i.startswith("compute"):
                functions.append(i)
        properties = []
        for func in functions:
            properties.append(Properties.__dict__[func](self,list_values))
        self.property = self.norm(properties)

    def norm(self,properties):
        return (sum([x**2 for x in properties])) ** 0.5

    def _compute_mean(self,list_values):
        return sum(list_values)/float(len(list_values))

    def bin_search(self,list_,value):
        low , high = 0, len(list_)
        while low<=high:
            mid = (low+high)//2
            if list_[mid][0]<= value <= list_[mid][1] :
                return list_[mid]
            elif list_[mid][0] < value:
                low = mid + 1
            else:
                high=mid -1

    def _discretize(self,list_values):
        _min = math.floor(min(list_values))
        _max = math.ceil(max(list_values))
        num_partitions = 100
        step = (_max - _min) / num_partitions
        start = _min
        counts = {(start + i*step, start + (i + 1) * step):0 for i in range(num_partitions)}
        keys = sorted(counts.keys())
        for element in list_values:
            range_ = self.bin_search(keys, element)
            counts[range_] +=1
        return counts


    def compute_entropy(self,list_values):
        if self.discrete:
            list_values = self._discretize(list_values).values()
            sum_array = sum(list_values)
            result = sum([i / sum_array * math.log(i / sum_array) for i in list_values if i!=0])
        else:
            result = sum([i*math.log(i) for i in list_values if i!=0])
        return result

    def compute_variance(self,list_values):
        mean = self._compute_mean(list_values)
        summ = 0
        for i in list_values:
            summ += (i-mean)**2
        return summ/float(len(list_values))

    def compute_perplexity(self,list_values):
        if self.discrete:
            return 0
        else:
            return math.exp(-self.compute_entropy(list_values))

    def compute_lorenz_measure(self,list_values):
        #TODO : Implement lorenz measure for list of values.
        measure = 0
        return measure