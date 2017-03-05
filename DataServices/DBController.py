from pymongo import MongoClient
import pprint

from DataServices.DataBlock import DataBlock


class CensusDB:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.Census
        self.coll = self.db.dataset

    def sampledRead(self, number = 10000, save = False):
        #sampled read is for our experiments
        datablock = DataBlock(list([i for i in self.coll.aggregate([{"$sample": {"size": number}}])]),
                  name="Resources/sample_{}.pkl".format(number))
        if save:
            datablock.save()
        return datablock

    def conditionRead(self,  fields= [], id = None, debug = False):

        id_dict = {} if id is None else {"_id": {"$in":id}}
        field_dict = {field:1 for field in fields}
        if len(field_dict)>0:
            field_dict["id"] = 1
        if debug and len(field_dict)>0:
            field_dict["Vil_Nam"] = 1
            field_dict["Stat_Nam"] = 1
        if debug:
            return DataBlock(list(self.coll.find(id_dict,field_dict).limit(200)),"")
        else:
            return DataBlock(list(self.coll.find(id_dict,field_dict)),"")

    def writeMultiple(self,data,cleanDB):
        """
        writes multiple datum objects into mongodb
        :param data: list of datum objects
        :return:
        """
        f = open("DEBUG.log", "w")
        if cleanDB:
            self.db.dataset.drop()
            self.coll = self.db.dataset
        print((len(data)))
        count = 0
        thresh = 1
        print("Writing to DB")
        for datum in data:
            try:
                self.coll.insert_one(datum.__dict__)
                count += 1
                perc = count/float(len(data))*100
                if perc>=thresh:
                    print(("{} perc completed".format(perc)))
                    thresh += 1
            except Exception as e:
                print(e)
                f.write(str(datum.__dict__))
        f.close()


if __name__=="__main__":
    dao = CensusDB()
    #dao.writeMultiple([{"test":"testing"},{"test1":"testing2"}])
    dao.sampledRead()
    # for i in cur:
    #     print i

