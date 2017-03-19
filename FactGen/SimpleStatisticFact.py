import pickle
import pprint
import random
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import json
from collections import Counter
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
        list_ids = set([(i[2]["id"]) for i in list_objects_r])
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

def perc_filter(l,perc=0.9):
    thresh = sorted(list(set(l)))[int(perc*len(set(l)))]
    for ind,val in enumerate(l):
        if val<thresh:
            l[ind] = 0

########### Class ###########

class SimpleStatisticFact:
    def __init__(self):
        self.graph = pickle.load(open("Resources/graph.pkl","rb"),encoding="latin1")
        self.field = "Near_Vil_Tow_Nam_hav_Prim_School"
        self.ignore = ["","N.A."]
        #self.fields = ["Hos_Allop_Num","Hos_Allop_Doc_Tot_Stren_Num"]
        field = copy.deepcopy(self.field)
        #self.choose_fields()
        print("Initialization Done. Reading from DB...")
        self.db_instance = CensusDB()
        self.datablock = self.db_instance.conditionRead(fields=[self.field],debug=False)
        print("DB Read Done. Mapping Atomic Fact...")
        self.generate_list()
        print("Computing Metric..")
        if self.field in numeric_fields:
            self.metric = (QuartileDeviation.compute(self.list))
        else:
            counter = Counter(self.list)
            l = list((counter.values())) #gets counts of each of the discrete value
            temp_metric = (QuartileDeviation.compute(l))
            self.metric = [temp_metric[l.index(counter[i])] for i in self.list]
        perc_filter(self.metric)
        print("Loading Partitions...")
        self.partitions = json.load(open("Resources/partitions.json"))
        #filtering to get interesting results; sorted by value of interestingness
        self.results = [x for x in sorted(zip(self.metric,self.list,self.datablock.list_dicts), key = lambda x: x[0],reverse=True) if x[0]!=0]
        self.print_facts_augmented_with_similarity()

    def is_similar(self, tuple1, tuple2):
        metric1, atom1, obj1 = tuple1
        metric2, atom2, obj2 = tuple2
        if self.field in numeric_fields:
            if 0.9*atom1<=atom2<=1.1*atom1:
                return True
        else:
            return atom1 == atom2


    def fuzzy_intersection(self):

        # For each list of villages
        #   For each field
        #       1. get global perc
        #       2. get local perc
        #   compute properties of each partition
        #   choose interesting partition(s)
        #   generate facts
        list_similar = copy.deepcopy(self.list_similar)
        discrete_fields.remove("Vil_Nam")
        #p = Pool(10)
        p = ProcessPoolExecutor(10)
        l = []
        f = open("Resources/Facts_data.json","w")
        for list_objects in list_similar:
            fact_dict = {}
            curr = list_objects[0]
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
            perc = len(list_objects) / float(len(self.datablock.list_dicts)) * 100
            print("Partitions got. Flattening...")
            flattened = list(map(flatten, partitions_perc))
            print("Flattening Done. Getting Properties...")
            properties = list(map(get_property, flattened))
            interestingnesses = QuartileDeviation.compute(properties)
            max_indices = [np.argmax(interestingnesses)]#np.argpartition(interestingnesses, -2)[-2:]

            #max_indices[np.argsort(interestingnesses[max_indices])]

            for max_index in max_indices:
                value_global_local = partitions_perc[max_index]
                field = args[max_index][0]
                fact_dict["data"] = [(self.field,(curr[2][self.field])),curr[1]]
                fact_dict["perc"] = perc
                fact_dict["value_global_local"] = value_global_local
                fact_dict["partition_field"] = field
                print(("{} perc(or {} num of villages) of villages have {} equal to {}".format(perc, len(list_objects),
                                                                                               self.field,
                                                                                               curr[1])))
                print("Field :\t",field)
                l.append(fact_dict)
                temp_dict = {i:value_global_local[i] for i in value_global_local if value_global_local[i]["global_perc"]}
                pprint.pprint(temp_dict,indent=2)
        f.write(json.dumps(l))
        f.close()
        print("####DONE####")
        p.shutdown()


        # global intersection
        # list_similar = self.list_similar
        # partition_list = []
        # print len(list_similar)
        # for list_objects in list_similar:
        #     def intersection(key):
        #         """
        #         :param key:
        #         :return: partitions list_objects on values of key: {value: number of villages}
        #          400 keys- partition... we must choose best keys... so we need some metric... we'll compute entropy
        #          H(X) = sigma over x epsilon X (p(x)*log(p(x))
        #          for every key, we'll get an entropy... Now, we'll apply interestingness measure on top of this!
        #          hypothesis: if entropy is interesting, then that key will give us interesting facts..
        #         """
        #         values = map(lambda x: x[2][key], list_objects)
        #         return Counter(values)
        #     p = Pool(5)
        #     partitions = p.map(intersection,discrete_fields)
        #     entropies = map(lambda x:Entropy.compute(x.values()),partitions)
        #     interestingness_partition = QuartileDeviation.compute(entropies)
        #     results = zip(discrete_fields,partitions,interestingness_partition)
        #     results = filter(lambda x:x[2]!=0,results)
        #     curr = list_objects[0]
        #     perc = len(list_objects) / float(len(self.results)) * 100
        #     if curr[1] == self.max:
        #         print "{} perc of villages have {} {} and {} {}.".format(perc,
        #                                                                  curr[2][self.fields[0]], self.fields[0],
        #                                                                  curr[2][self.fields[1]], self.fields[1])
        #     else:
        #         print "{} perc of villages have {} to {} ratio of {} with one of them having {} {} and {} {}.".format(
        #             perc,
        #             self.fields[0], self.fields[1],
        #             curr[1], curr[2][self.fields[0]], self.fields[0],
        #             curr[2][self.fields[1]], self.fields[1])
        #     for result in results:
        #         field, partitions, interestingness_partition = result
        #         total = sum(partitions.values())
        #         temp_list = partitions.most_common()
        #         max_value, max_count = temp_list[0]
        #         min_value, min_count = temp_list[-1]
        #         perc_1 = max_count/float(total)*100
        #         if perc_1 > 90:
        #             print "\tInterestingly, about {} perc of these villages have {} equal to {}.".format(perc_1,field,max_value)
        #         # perc_1 = min_count/float(total)
        #         # print "\tNotably, only {} perc of these villages have {} equal to {}.".format(perc_1,field,min_value)
        #     #raw_input()
        #     print "done"

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
            print(("{} perc(or {} num of villages) of villages have {} equal to {}".format(perc,similarity_count,
                                                                            self.field,
                                                                        curr[1])))
            f.write("======================\n")
            f.write(pprint.pformat(new_similar_set, indent=4))
            f.write("\n=======================\n")
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

    def choose_fields(self):
        list_fields = [fields for fields in self.graph.top_percentile_graph_ds if not (fields[0].endswith("Stat") or fields[1].endswith("Stat")) and not (fields[0].startswith("Dist") or fields[1].startswith("Dist")) and not ("Doc" in fields[0] or "Doc" in fields[1]) and (fields[0] in numeric_fields or fields[1] in numeric_fields)]
        self.fields = random.choice(list_fields)

    def generate_list(self):
        self.list = self.datablock.extract(self.field)
        self.list = list(filter(lambda x:x.strip() not in self.ignore, self.list))