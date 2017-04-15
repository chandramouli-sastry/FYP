"""
Take property and similarity between perc
"""
import pickle
import pprint
import random
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import json
from collections import Counter

from FactPrinter import identify_dominance, num_villages
from FactPrinter.QuartileCalculation import quartiles
from Properties.Properties import Properties
from collections import Counter
from multiprocessing import Pool
import numpy as np
from DataServices.DBController import CensusDB
from Metrics import Entropy
from Metrics import Grubbs
from Resources import numeric_fields,convert, continuous_fields, discrete_fields
from Metrics import QuartileDeviation
import copy

########### Functions for Pool ###########
def global_local(field, partitions, list_objects_r):
    value_global_local = {}
    try:
        list_ids = set([(i[-1]["id"]) for i in list_objects_r])
        for value in partitions:
            list_objects = partitions[value]
            count = len(set(list_objects) & list_ids)
            global_perc = count / float(len(list_objects))
            local_perc = count / float(len(list_objects_r))
            value_global_local[value] = {"global_perc": global_perc, "local_perc": local_perc}
    except Exception as e:
        print((field, e))
    return value_global_local


def global_local_multi(field_list):
    return global_local(*field_list)

def flatten(partition):
    l = []
    for global_local_dict in list(partition.values()):
        l.extend(list(global_local_dict.values()))
    return l

def get_property(values_list):
    return Properties(values_list).property

def perc_filter(l,perc=0):
    return
    if len(l)- l.count(0)>150:
        thresh = sorted(set(l),reverse=True)[150]
        for ind,val in enumerate(l):
            if val<=thresh:
                l[ind] = 0

def get_thresh(list_values, perc):
    return sorted(list_values)[int(perc*len(list_values))]

########### Class ###########

class SemanticStatisticFact:
    def __init__(self,field,fileName,debug=False,print_=False):
        self.field = field
        field = self.field
        self.fileName = fileName
        self.print = print_
        self.ignore = ["","N.A.","null"]
        #self.fields = ["Hos_Allop_Num","Hos_Allop_Doc_Tot_Stren_Num"]
        self.ontology = pickle.load(open("Resources/ontology.pkl","rb"),encoding="latin1")
        self.child_fields = list(map(lambda x:x[0],self.ontology.get_children(self.field)))
        child_fields = copy.deepcopy(self.child_fields)
        #self.choose_fields()
        print("Initialization Done. Reading from DB...")
        self.db_instance = CensusDB()
        self.datablock = self.db_instance.conditionRead(fields=self.child_fields+[self.field],debug=debug)
        print("DB Read Done. Mapping Atomic Fact...")
        global get_prop
        def get_prop(obj):
            return Properties(list(map(lambda x: obj[x]/obj[field] if obj[field]!=0 else 9999, child_fields)), discrete= False, ordering=True).property
            #return obj[child_fields[0]]/obj[field] if obj[field]!=0 else 9999
        self.get_prop = get_prop
        self.generate_list()
        print("Computing Metric..")
        counter = Counter(self.list)  # village_name -> count
        l = list((counter.values()))  # gets counts of each of the discrete value

        # cluster points in l
        partitions = identify_dominance(list(set(l)))
        counter_count = {}
        for start, end, mean in partitions:
            count = 0
            values = []
            for value in l:
                if start <= value <= end:
                    values.append(value)
                    count += 1
            counter_count[mean] = (count, values)
        x = sorted(counter_count.values())
        sum_so_far = 0
        idx = 0
        metric = {}
        quartile = sorted(l)[3 * len(l) // 4]
        while sum_so_far <= 150 and idx < len(x):
            count, values = x[idx]
            for value in values:
                metric[value] = abs(value - quartile + 1) # convert to percentage
            sum_so_far += count
            idx += 1

        self.metric = [metric.get(counter[i], 0) for i in self.list]
        #self.metric = [max(percentages[i],1-percentages[i])* (counter[i]-q1+1 if counter[i]<=q1 else (q3-counter[i]+1 if q3<counter[i] else 0)) for i in self.list]
        #self.metric = (QuartileDeviation.compute(self.list))
        perc_filter(self.metric)
        #filtering to get interesting results; sorted by value of interestingness
        self.results = [x for x in sorted(zip(self.metric, self.values_list,self.list,self.datablock.list_dicts), key = lambda x: x[0],reverse=True) if x[0]!=0]
        self.print_facts_augmented_with_similarity()

    def is_similar(self, tuple1, tuple2):
        metric1, atom_list, atom1, obj1 = tuple1
        metric2, atom_list, atom2, obj2 = tuple2
        return atom1 == atom2

    def get_statement(self,curr,perc,count):
        metric, atom_list, atom, obj = curr
        binarize = lambda x: (x != 9999 and x != 0) * 1
        if atom==9999:
            return ("{} perc(or {} num of villages) of villages have {} equal to {}".format(perc,count,
                                                                            self.field,
                                                                        0))
        else:
            return ("{} perc(or {} num of villages) of villages have {} and do not have {}".format(perc,count,
                                                                                [field for field,value in zip(self.child_fields,atom_list) if binarize(value[1])],[field for field,value in zip(self.child_fields,atom_list) if not(binarize(value[1]))]
                                                                        ))

    def fuzzy_intersection(self):

        # For each list of villages
        #   For each field
        #       1. get global perc
        #       2. get local perc
        #   compute properties of each partition
        #   choose interesting partition(s)
        #   generate facts
        print("FUZZY INTERSECTION")
        list_similar = copy.deepcopy(self.list_similar)
        discrete_fields.remove("Vil_Nam") if "Vil_Nam" in discrete_fields else None
        #p = Pool(10)
        p = ProcessPoolExecutor(10)
        l = []
        f = open(self.fileName,"w")
        for list_objects in list_similar:
            fact_dict = {}
            curr = list_objects[0]
            if len(list_objects)>20:
                args = [(field,self.partitions[field],list_objects) for field in discrete_fields if field in self.partitions]
                print(("Args Ready.", len(args)))
                partitions_perc = []
                count = 0
                thresh = 1
                for arg in args:
                    partitions_perc.append(global_local_multi(arg))
                    # count += 1
                    # perc = count/len(args)*100
                    # if perc>thresh:
                    #     print(perc)
                    #     thresh += 1
                perc = len(list_objects) / float(num_villages) * 100
                print("Partitions got. Flattening...")
                flattened = list(map(flatten, partitions_perc))
                print("Flattening Done. Getting Properties...")
                properties = list(map(get_property, flattened))
                interestingnesses = QuartileDeviation.compute(properties)
                max_indices = [np.argmax(interestingnesses)]#np.argpartition(interestingnesses, -2)[-2:]
            else:
                perc = len(list_objects) / float(len(self.datablock.list_dicts)) * 100
                max_indices = [None]
            for max_index in max_indices:
                value_global_local = partitions_perc[max_index] if max_index!=None else {}
                field = args[max_index][0] if max_index!=None else None
                fact_dict["data"] = [(self.field,self.child_fields),curr[1]]
                fact_dict["perc"] = perc
                fact_dict["metric"] = max(perc,100-perc) * curr[0]
                fact_dict["Vil_Nam"] = curr[-1]["Vil_Nam"]
                fact_dict["Stat_Nam"] = curr[-1]["Stat_Nam"]
                temp_dict = {i: value_global_local[i] for i in value_global_local if
                             value_global_local[i]["global_perc"]}
                fact_dict["value_global_local"] = temp_dict
                fact_dict["partition_field"] = field
                l.append(fact_dict)
                if self.print:
                    print(("{} perc(or {} num of villages) of villages have {} equal to {}".format(perc, len(list_objects),
                                                                                                   self.child_fields,
                                                                                                   curr[1])))
                    print("Field :\t",field)
                    pprint.pprint(temp_dict,indent=2)
        f.write(json.dumps(l))
        f.close()
        print("####DONE####")
        p.shutdown()

    def print_facts_augmented_with_similarity(self):
        total_set = set(range(len(self.results)))
        '''
         [Vil1, Vil2 ...... Viln]; Vil0-Ref Village
         Vil0 and compare with all of them and see if there is similarity; if there is, increment count of similarity
         Vil0, Vil3,...k such villages
         Vil0

        '''
        f = open("DEBUG.log","w")
        list_similar = []
        visited_set = set()
        max_count = 150
        while visited_set != total_set:
            to_visit = total_set-visited_set
            index = list(to_visit)[0]
            visited_set.add(index)
            curr = self.results[index]
            similarity_count = 1
            new_similar_set = [curr]

            for index,result in enumerate(self.results):
                if index not in visited_set:
                    if self.is_similar(curr,result):
                        similarity_count += 1
                        visited_set.add(index)
                        new_similar_set.append(result)
            list_similar.append(new_similar_set)
            perc = similarity_count / float(len(self.datablock.list_dicts))*100
            if self.print:
                print(self.get_statement(curr,perc,similarity_count))
            f.write("======================\n")
            f.write(pprint.pformat(new_similar_set, indent=4))
            f.write("\n=======================\n")
            if (len(list_similar) == max_count):
                break
        f.close()
        self.list_similar = list_similar


    def print_facts(self,number = 10):
        fields = [self.field]
        print((fields[0]))
        count = 0
        for score,ratio,_dict in self.results:
            print(score)
            print((_dict["Vil_Nam"]))
            print((_dict[fields[0]]))
            print((_dict[fields[1]]))
            count += 1
            if count==number:
                break


    def generate_list(self):
        self.list = self.datablock.apply(self.get_prop)
        self.values_list = [[(obj[x],obj[x]/obj[self.field] if obj[self.field]!=0 else 9999) for x in self.child_fields] for obj in self.datablock.list_dicts]
        # self.field_perc = []
        # idx = 0
        # field_list = self.child_fields
        # for obj in self.datablock.list_dicts:
        #     perc_list = list(map(lambda x:x[1],self.values_list[idx]))
        #     partitions = identify_dominance(perc_list)
        #     fieldP_dict = {}
        #     for index,i in enumerate(perc_list):
        #         for start,end,mean in partitions:
        #             if start <= i <= end:
        #                 fieldP_dict[field_list[index]] = mean
        #                 break
        #     self.field_perc.append(fieldP_dict)
        #     idx += 1

