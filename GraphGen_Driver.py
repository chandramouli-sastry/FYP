from DataServices.DBController import CensusDB
from DependencyGraphGen.GeneratePairs import gen_graph
from Resources import *

import pickle

# CONFIG
db = CensusDB()
#db.sampledRead(number=100,save=True)
dataBlock = pickle.load(open("Resources/sample_100.pkl"))
graph = gen_graph(fields,new_fields,ontology,dataBlock)
for field1,field2 in graph.top_percentile_graph_ds:
    print field1,field2
