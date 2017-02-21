import pickle
import random

from DataServices.DBController import CensusDB
from Resources import numeric_fields,convert
from Metrics import QuartileDeviation


class NumericRatioFact:
    def __init__(self):
        self.graph = pickle.load(open("Resources/graph.pkl"))
        self.choose_fields()
        self.max = 9999
        global compute_ratio
        def compute_ratio(object):
            denom = convert(object[self.fields[1]])
            if denom == 0:
                return 9999
            else:
                return convert(object[self.fields[0]])/denom
        self.compute_ratio = compute_ratio
        print "Initialization Done. Reading from DB..."
        self.datablock = CensusDB().sampledRead(number=20000)
        print "DB Read Done. Computing Ratios..."
        self.generate_list()
        print "Computing Metric.."
        self.metric = QuartileDeviation.compute(self.list)
        self.result = sorted(zip(self.metric,self.list,self.datablock.list_dicts), key = lambda x: x[0],reverse=True)

    def print_facts(self,number = 10):
        fields = self.fields
        print fields[0],fields[1]
        count = 0
        for score,ratio,_dict in self.result:
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
