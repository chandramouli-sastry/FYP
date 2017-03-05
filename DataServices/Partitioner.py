import pickle

from DataServices.DBController import CensusDB
from DataServices.MapReduce import MapReduce
from .fields_partition import fields

class Partitioner:
    def __init__(self, fileReader, code_id):
        self.db = CensusDB()
        self.code_id = code_id
        self.objs = []
        while True:
            new_obj = fileReader.next_line()
            if new_obj == False:
                break
            self.objs.append(new_obj)


    def partition(self,field = None):

        code_id = self.code_id
        if field == None:
            global map_function
            def map_function(obj):
                if obj["Vil_Cod"] not in code_id:
                    return []
                op_list = []
                for field in fields:
                    op_list.append((field+":"+obj[field],code_id[obj["Vil_Cod"]]))
                return op_list
        else:
            global map_function
            def map_function(obj):
                if obj["Vil_Cod"] not in code_id:
                    return []
                op_list = []
                op_list.append((field+":"+obj[field],code_id[obj["Vil_Cod"]]))
                return op_list
        global reduce_function

        def reduce_function(item):
            return item[0],item[1]

        mapper = MapReduce(map_function,reduce_function,num_workers=5)
        results = mapper(self.objs)
        with open("Resources/results.pkl","w") as f:
            pickle.dump(results,f)