import pickle
import signal
import threading
from threading import Thread

from pymongo import MongoClient
from Resources import discrete_fields
from bson.code import Code
from bson.son import SON
client = MongoClient()
db = client.Census
coll = db.dataset
field_value_ids = {}
#discrete_fields= ["Stat_Nam"]
import time
discrete_fields.pop(discrete_fields.index("Vil_Nam"))
for field in discrete_fields:#field- loop over all discrete fields
    try:
        t= time.time()
        print(field, end=' ')
        x = input("Run for this field(y/n)?")
        if x!="y":
            raise Exception("Wont Do")
        res = coll.map_reduce(
            Code("""
                        function(){
                            var id= this.id.toString();
                            for(var field in fields)
                            {
                                field = fields[field];
                                emit(field+","+(this[field]).toString(),id);
                            }
                        }
                        """),
            Code("""
                        function(key,values)
                        {
                            return values.join(",");
                        }
                        """),
            out=SON([("inline", 1)]),  # SON([("replace","temp")]),
            scope=SON([("fields", discrete_fields)]),
            finalize=Code("""function(key,reducedVal){
                        return reducedVal.split(",").map(function(x){return x*1});
                    }"""),
            jsMode=True
        )
        list_values = res["results"]  # .find()#
        value_ids = {}
        for item in list_values:
            value = item["_id"]
            ids = item["value"]
            value_ids[value] = ids
        print(sum(map(len,list(value_ids.values()))))
        field_value_ids[field] = value_ids
        print(field, "DONE", time.time()-t)

    except Exception as e:
        print(e)
        print(field, "NOT DONE")

dump = pickle.dumps(field_value_ids)
print(len(dump))
with open("Resources/partitions_1.pkl","w") as f:
    f.write(dump)

