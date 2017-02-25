class Properties:

    def _computeMean(self,list_values):
        return sum(list_values)/float(len(list_values))


    def computeVariance(self,list_values):
        mean = _computeMean(list_values)
        summ = 0
        for i in list_values:
            summ += (i-mean)**2
        return summ/float(len(list_values))

