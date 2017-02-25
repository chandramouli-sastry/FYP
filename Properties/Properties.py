class Properties:

    def _compute_mean(self,list_values):
        return sum(list_values)/float(len(list_values))


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