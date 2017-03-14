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
sorted = sorted(zipped,key = lambda x:x[-1], reverse=True)
for fields,value in sorted:
    if fields[0] in continuous_fields and fields[1] in continuous_fields:
        print((fields,value))
