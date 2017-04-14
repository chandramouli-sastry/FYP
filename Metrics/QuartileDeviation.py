def compute_Q1_Q2(array):
    temp = sorted(array)
    # mean = sum(array)/len(temp)
    # mean_index = 0
    # for ind,val in enumerate(temp):
    #     if val>=mean:
    #         mean_index = ind
    #         break
    # q1 = sum(temp[:mean_index+1])/len(temp[:mean_index+1])
    # q2 = sum(temp[mean_index+1:])/len(temp[mean_index+1:])
    q1 = temp[len(temp)//4]
    q2 = temp[3*len(temp)//4]
    iqr = q2-q1
    q1 = q1 - 1.5*iqr
    q2 = q2 + 1.5*iqr
    return q1,q2

def compute(array):
    Q1_value,Q2_value = compute_Q1_Q2(array)
    result = list()
    for i in array:
        if i<=Q1_value:
            result.append((Q1_value+1-i)/Q1_value)
        elif i>=Q2_value:
            result.append((i-Q2_value+1)/Q2_value)
        else:
            result.append(0)
    return result