from DataServices.DBController import CensusDB
from DependencyGraphGen.GeneratePairs import gen_graph
from Resources import *
import pickle

# CONFIG
#dataBlock = pickle.load(open("Resources/sample_100.pkl"))
create = False
if create:
    db = CensusDB()
    dataBlock = db.sampledRead(number=50000, save=True, fields=numeric_fields)
    print("READ and SAVE DONE")
    graph = gen_graph(numeric_fields,[],ontology,dataBlock)
    with open("Resources/graph.pkl","wb") as f:
        pickle.dump(graph, f)
else:
    graph = pickle.load(open("Resources/graph.pkl","rb"))

field_pairs = list(graph.top_percentile_graph_ds.keys())
values = [graph.get_value(x[0],x[1]) for x in field_pairs]
zipped = list(zip(field_pairs, values))
sorted_ = sorted(zipped,key = lambda x:x[-1], reverse=True)
s = set()
for fields,value in sorted_:
    if fields[0] in continuous_fields and fields[1] in continuous_fields:
        s.add(tuple(sorted(fields)))
l = [(graph.get_value(i,j),i,j) for i,j in s]
print(sorted(l,reverse=True))
for i,j,k in sorted(l,reverse=True):
    print(i,j,k)

