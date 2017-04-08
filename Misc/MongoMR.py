import pickle
from pymongo import MongoClient
from Resources import discrete_fields
from bson.code import Code
from bson.son import SON
client = MongoClient()
db = client.Census
coll = db.dataset
field_value_ids = {}
#discrete_fields= ["Stat_Nam"]

for field in discrete_fields:#field- loop over all discrete fields
    try:
        res = coll.map_reduce(
            Code("""
            function(){
                var id= ""+this.id;
                emit(this[field],id);
            }
            """),
            Code("""
            function(key,values)
            {
                return values.join(",");
            }
            """),
            out = SON([("replace","temp")]),
            scope = SON([("field",field)]),
            finalize = Code("""function(key,reducedVal){
            return reducedVal.split(",").map(function(x){return x*1});
        }""")
        )
        list_values = res.find()#["results"]
        value_ids = {}
        for item in list_values:
            value = item["_id"]
            ids = item["value"]
            value_ids[value] = ids
        field_value_ids[field] = value_ids
        print(field, "DONE")
        #print(field_value_ids[field_value_ids.keys()[0]][field_value_ids[field_value_ids.keys()[0]].keys()[0]])
    except Exception as e:
        print(e)
        print(field, "NOT DONE")
import json
with open("Resources/partitions_new.json","w") as f:
    json.dump(field_value_ids,f)
#create object like field:{value_of_field:list_of_ids}
import pprint
#pprint.pprint(field_value_ids)
