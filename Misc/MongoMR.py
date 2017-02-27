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
                var id= this._id.toString();
                id = id.slice(id.indexOf('"')+1,id.lastIndexOf('"'));
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
            finalize = Code("""function(key,reducedVal) {
                    return reducedVal.split(",");
                }""")
        )
        list_values = res.find()#["results"]
        value_ids = {}
        for item in list_values:
            value = item["_id"]
            ids = item["value"]
            value_ids[value] = ids
        field_value_ids[field] = value_ids
        print field, "DONE"
    except Exception as e:
        print e
        print field, "NOT DONE"

dump = pickle.dumps(field_value_ids)
print len(dump)
with open("Resources/partitions.pkl","wb") as f:
    f.write(dump)
#create object like field:{value_of_field:list_of_ids}
import pprint
#pprint.pprint(field_value_ids)
