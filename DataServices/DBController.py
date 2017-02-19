from pymongo import MongoClient
import pprint

from DataServices.DataBlock import DataBlock


class CensusDB:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.Census
        self.coll = self.db.dataset

    def sampledRead(self, number = 10000, save = False):
        DataBlock(list([i for i in self.coll.aggregate([{ "$sample": { "size": number } }])]),name="Resources/sample_{}.pkl".format(number))

    def writeMultiple(self,data,cleanDB):
        """
        writes multiple datum objects into mongodb
        :param data: list of datum objects
        :return:
        """
        if cleanDB:
            self.db.dataset.drop()
            self.coll = self.db.dataset
        print len(data)
        for datum in data:
            self.coll.insert_one(datum.__dict__)


if __name__=="__main__":
    dao = CensusDB()
    #dao.writeMultiple([{"test":"testing"},{"test1":"testing2"}])
    dao.sampledRead()
    # for i in cur:
    #     print i

