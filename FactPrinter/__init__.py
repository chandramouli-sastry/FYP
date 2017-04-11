import math
import random

num_villages = 622725
def perplexity(l):
    s = 0
    d = sum(l)
    if d==0:
        return 1
    for i in l:
        i = i/d
        s += i*math.log(i,2) if i!=0 else 0
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
            list_lists.append((temp_list[0],temp_list[-1],sum(temp_list)/len(temp_list)))
            temp_list = [i]
    list_lists.append((temp_list[0], temp_list[-1], sum(temp_list) / len(temp_list)))
    return (list_lists)

def get_fields_to_print(field_list):
    max_fields_to_show = 5
    min_count = 5
    count = len(field_list)
    if (count - max_fields_to_show) > min_count:
        to_sample = max_fields_to_show
    elif  count<max_fields_to_show:
        to_sample = count
    else:
        to_sample = count - min_count
    #return (", ".join(random.sample(field_list,to_sample)),count-to_sample)
    return (", ".join(field_list[:to_sample]),count-to_sample)

def global_local_analysis(field_name, global_local_dict):
    global_local_dict = {i: global_local_dict[i] for i in global_local_dict if
                         global_local_dict[i]["global_perc"]}
    if len(global_local_dict)==1:
        partition_value = global_local_dict.keys()[0]
        return "in_place","having {} equal to {}".format(field_name,partition_value)
    else:
        pass


identify_dominance([30,40,30])
identify_dominance([30,70])
identify_dominance([10,12,15,100-12-15-10])