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
def work():
    global res,tid,ran
    tid = threading.current_thread()
    res = coll.map_reduce(
        Code("""
                function(){
                    var id= this.id.toString();
                    emit(this[field],id);
                }
                """),
        Code("""
                function(key,values)
                {
                    return values.join(",");
                }
                """),
        out=SON([("inline", 1)]),  # SON([("replace","temp")]),
        scope=SON([("field", field)]),
        finalize=Code("""function(key,reducedVal){
                return reducedVal.split(",").map(function(x){return x*1});
            }""")
    )
    ran = True


import time
for field in discrete_fields:#field- loop over all discrete fields
    try:
        t= time.time()
        thread = Thread(target=work)
        thread.start()
        thread.join(60)
        signal.pthread_kill()
        
        if ran:
            list_values = res["results"]  # .find()#
            value_ids = {}
            for item in list_values:
                value = item["_id"]
                ids = item["value"]
                value_ids[value] = ids
            field_value_ids[field] = value_ids
            print((field, "DONE", time.time()-t))
        else:
            raise Exception("Couldnt do")
    except Exception as e:
        print(e)
        print((field, "NOT DONE"))

dump = pickle.dumps(field_value_ids)
print((len(dump)))
with open("Resources/partitions_1.pkl","w") as f:
    f.write(dump)
#create object like field:{value_of_field:list_of_ids}
import pprint
#pprint.pprint(field_value_ids)