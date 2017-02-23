import pickle
import random

from DataServices.DBController import CensusDB
from Resources import numeric_fields,convert
from Metrics import QuartileDeviation

class NumericRatioFact:
    def __init__(self):
        self.graph = pickle.load(open("Resources/graph.pkl"))
        self.fields = ["Tot_Fem_Pop_of_Vil","Tot_Mal_Pop_of_Vil"]
        #self.choose_fields()
        self.max = 9999
        global compute_ratio
        def compute_ratio(object):
            denom = convert(object[self.fields[1]])
            if denom == 0:
                return self.max
            else:
                return convert(object[self.fields[0]])/float(denom)
        self.compute_ratio = compute_ratio
        print "Initialization Done. Reading from DB..."
        self.datablock = CensusDB().sampledRead(number=30000)
        print "DB Read Done. Computing Ratios..."
        self.generate_list()
        print "Computing Metric.."
        self.metric = QuartileDeviation.compute(self.list)
        #filtering to get interesting results; sorted by value of interestingness
        self.results = filter(lambda x: x[0]!=0,sorted(zip(self.metric,self.list,self.datablock.list_dicts), key = lambda x: x[0],reverse=True))
        self.print_facts_augmented_with_similarity()

    def is_similar(self, tuple1, tuple2):
        metric1, ratio1, obj1 = tuple1
        metric2, ratio2, obj2 = tuple2
        if ratio1-0.1<=ratio2<=ratio1+0.1:
            return True


    def fuzzy_intersection(self):
        list_similar = self.list_similar
        for similar_items in list_similar:
            pass

    def print_facts_augmented_with_similarity(self):
        total_set = set(range(len(self.results)))
        '''
         [Vil1, Vil2 ...... Viln]; Vil0-Ref Village
         Vil0 and compare with all of them and see if there is similarity; if there is, increment count of similarity
         Vil0, Vil3,...k such villages
         Vil0

        '''
        list_similar = []
        visited_set = set()
        while visited_set != total_set:
            to_visit = total_set-visited_set
            index = list(to_visit)[0]
            visited_set.add(index)
            curr = self.results[index]
            list_similar.append(curr)
            similarity_count = 0
            new_similar_set = set([curr])
            for index,result in enumerate(self.results):
                if index not in visited_set:
                    if self.is_similar(curr,result):
                        similarity_count += 1
                        visited_set.add(index)
                        new_similar_set.add(result)
            list_similar.append(new_similar_set)
            perc = similarity_count / float(len(self.results))*100
            if perc > 0:
                if curr[1] == self.max:
                    print "{} perc of villages have {} {} and {} {}".format(perc,
                                                                            curr[2][self.fields[0]], self.fields[0],
                                                                            curr[2][self.fields[1]], self.fields[1])
                else:
                    print "{} perc of villages have {} to {} ratio of {} with one of them having {} {} and {} {}".format(perc,
                                                                            self.fields[0], self.fields[1],
                                                                        curr[1], curr[2][self.fields[0]], self.fields[0],
                                                                            curr[2][self.fields[1]], self.fields[1])
        self.list_similar = list_similar


    def print_facts(self,number = 10):
        fields = self.fields
        print fields[0],fields[1]
        count = 0
        for score,ratio,_dict in self.results:
            print score
            print _dict["Vil_Nam"]
            print _dict[fields[0]]
            print _dict[fields[1]]
            count += 1
            if count==number:
                break

    def choose_fields(self):
        list_fields = [fields for fields in self.graph.top_percentile_graph_ds if not (fields[0].endswith("Stat") or fields[1].endswith("Stat")) and not (fields[0].startswith("Dist") or fields[1].startswith("Dist")) and not ("Doc" in fields[0] or "Doc" in fields[1]) and (fields[0] in numeric_fields or fields[1] in numeric_fields)]
        self.fields = random.choice(list_fields)

    def generate_list(self):
        self.list = self.datablock.apply(self.compute_ratio)
