/**
 * Created by cshamasastry on 2/27/17.
 */

field = "Gram_Pan_Cod";
db.dataset.mapReduce(
    function(){
        var id= this._id.toString();
        id = id.slice(id.indexOf('"')+1,id.lastIndexOf('"'));
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

        "finalize" : function(key,reducedVal) {
            return reducedVal.split(",");
        }

    });
/*
list of documents:
  {_id: key , value: reduced-value}
db.dataset.aggregate(
   [ { $sample: { size: 20 } },{$project:{"Stat_Nam":1}},{$out:"sampledata"} ]
)
 */