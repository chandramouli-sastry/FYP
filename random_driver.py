#from Misc import MongoMR_1
from DataServices.DBController import CensusDB
from DataServices.FileReader import FileReader
from DataServices.Partitioner import Partitioner
from DataServices.fields_partition import fields
from Resources import mapping
#
# db = CensusDB()
# datablock = db.conditionRead(fields=["id","Vil_Cod"])
# code_id = {}
# for obj in datablock.list_dicts:
#     code_id[obj["Vil_Cod"]] = obj["id"]
# print "DB Read Done. Reading File"
# fileReader = FileReader("Data/full_data.txt",mapping)
# print "File Read Done. Creating Partitioner..."
# partitioner = Partitioner(fileReader, code_id)
# print "Partitioning..."
# for field in fields:
#     partitioner.partition(field)
#     print field,"Done"

import pickle,time
t = time.time()
pickle.load(open("Resources/partitions.pkl"))
print((time.time()-t))