
def compute(array):
    mean = sum(array)/len(array)
    return {i:(i-mean) for i in array}