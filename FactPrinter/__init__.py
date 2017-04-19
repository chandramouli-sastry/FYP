import math
import random
try:
    printer_mapping = eval(open("../FactPrinter/printer_mapping").read())
except Exception as e:
    printer_mapping = eval(open("FactPrinter/printer_mapping").read())
num_villages = 622725
INF = 9999
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
    if l==[]:
        return []
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


def print_binarize(param):
    return param.replace("Number of","").replace("Distance to","").replace("Total Strength","").replace("Nearest","Nearby").replace("Distance","").strip()


def global_local_analysis(field_name, global_local_dict):
    global_local_dict = {i: global_local_dict[i] for i in global_local_dict if
                         global_local_dict[i]["global_perc"]}
    if len(global_local_dict)==1:
        partition_value = global_local_dict.keys()[0]
        return "in_place","having {} equal to {}".format(field_name,partition_value)
    else:
        pass
def correct(x):
    if x.endswith("_C"):
        while x.endswith("_C"):
            x = x[:-2]
    return x

def get_fields_to_print(field_list,binarize=False):
    max_fields_to_show = 5
    min_count = 5
    if not(binarize):
        field_list = list(set([printer_mapping.get(correct(i),i) for i in field_list]))
    else:
        field_list = list(set([print_binarize(printer_mapping.get(correct(i),correct(i))) for i in field_list]))
    count = len(field_list)
    if (count - max_fields_to_show) > min_count:
        to_sample = max_fields_to_show
    elif  count<=max_fields_to_show:
        to_sample = count
    else:
        to_sample = count - min_count
    #return (", ".join(random.sample(field_list,to_sample)),count-to_sample)
    return (", ".join(field_list[:to_sample]),count-to_sample)


identify_dominance([30,40,30])
identify_dominance([30,70])
identify_dominance([10,12,15,100-12-15-10])