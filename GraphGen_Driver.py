from DataServices.DBController import CensusDB
from DependencyGraphGen.GeneratePairs import gen_graph
from Resources import *
import pickle

# CONFIG
db = CensusDB()
#db.sampledRead(number=100,save=True)
dataBlock = pickle.load(open("Resources/sample_100.pkl"))
create = False
if create:
    graph = gen_graph(numeric_fields,non_numeric_fields,ontology,dataBlock)
    with open("Resources/graph.pkl","wb") as f:
        pickle.dump(graph, f)
else:
    graph = pickle.load(open("Resources/graph.pkl"))

field_pairs = graph.top_percentile_graph_ds.keys()
values = map(lambda x:graph.get_value(x[0],x[1]),field_pairs)
zipped = zip(field_pairs, values)
sorted = sorted(zipped,key = lambda x:x[-1], reverse=True)
for fields,value in sorted[:100]:
    if not(fields[0].endswith("Stat") or fields[1].endswith("Stat")) and( fields[0] in numeric_fields or fields[1] in numeric_fields):
        print fields,value
