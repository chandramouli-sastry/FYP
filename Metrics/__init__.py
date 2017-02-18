import Deviation

class Metric:
    def __init__(self,module):
        self.compute_func = module.compute

    def quantify(self,values):
        set_values = zip(set(values),range(len(set(values))))
        map = {i:v for i,v in set_values}
        new_values = [map[i] for i in values]
        return new_values

    def compute(self,values):
        if type(values[0])==str:
            values = self.quantify(values)
        self.compute_func(values)

Deviation = Metric(Deviation)
