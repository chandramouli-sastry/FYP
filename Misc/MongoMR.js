/**
 * Created by cshamasastry on 2/27/17.
 */

field = "Stat_Nam";
db.dataset.mapReduce(
    function(){
        var id= "" + this.id;
        emit(this[field],id);
    },
    function(key,values)
    {
        return values.join(",");
    },
    {
        "out": {"replace":"temp"}/*{merge: "partition"}*/,
        "scope":{
            "field": field
        },

        "finalize" : function(key,reducedVal){
            return reducedVal.split(",").map(function(x){return x*1});
        }
    });
/*
list of documents:
  {_id: key , value: reduced-value}
db.dataset.aggregate(
   [ { $sample: { size: 20 } },{$project:{"Stat_Nam":1}},{$out:"sampledata"} ]
)
id = 0;
db.dataset.find().forEach(function(collection){collection["id"]=id++;db.dataset_new.insert(collection);if(id%2000==0)print(i);});

 */