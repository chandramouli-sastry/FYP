import math
num_villages = 622725
def perplexity(l):
    s = 0
    d = sum(l)
    for i in l:
        i = i/d
        s += i*math.log(i,2)
    return 2**(-s)

def identify_dominance(list_numbers):
    """
    :param list_numbers:
    :return: {"similarity" : which numbers are dominant and the percentages to use, "contrast" : dominant vs others}
    """
    l = sorted(list_numbers)
    list_lists = []
    temp_list = []
    perc = 0.05
    for i in l:
        temp_list.append(i)
        if perplexity(temp_list)<(1-perc)*len(temp_list):
            temp_list.pop(-1)
            list_lists.append((temp_list[0],temp_list[1],sum(temp_list)/len(temp_list)))
            temp_list = [i]
    list_lists.append((temp_list[0], temp_list[1], sum(temp_list) / len(temp_list)))
    return (list_lists)

def global_local_analysis(global_local_dict):
    pass


# identify_dominance([30,40,30])
# identify_dominance([30,70])
# identify_dominance([10,12,15,100-12-15-10])