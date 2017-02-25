from __future__ import division
def compute_Q1_Q2(array):
    temp = sorted(array)
    mean = sum(array)/len(temp)

    return temp[int((0.25)*len(temp))],temp[int((0.75*len(temp)))]

def compute(array):
    Q1_value,Q2_value = compute_Q1_Q2(array)
    result = list()
    for i in array:
        if i<=Q1_value:
            result.append(Q1_value-i)
        elif i>=Q2_value:
            result.append(i-Q2_value)
        else:
            result.append(0)
    return result