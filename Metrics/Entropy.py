
import math
def compute(array):
    sum_array = sum(array)
    result = sum([i/sum_array*math.log(i/sum_array) for i in array])
    return result