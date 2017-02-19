from pymongo import MongoClient
import pprint

class CensusDAO:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.Census
        self.coll = self.db.dataset

    def sampledRead(self, number = 10000, save = False):
        pprint.pprint(([i for i in self.coll.aggregate([{ "$sample": { "size": 4 } },{ "$project": { "Vil_Nam": 1, "Primary_School":1 } }])]))

    def writeMultiple(self,data):
        """
        writes multiple datum objects into mongodb
        :param data: list of datum objects
        :return:
        """
        for datum in data:
            self.coll.insert_one(datum.__dict__)


if __name__=="__main__":
    dao = CensusDAO()
    #dao.writeMultiple([{"test":"testing"},{"test1":"testing2"}])
    dao.sampledRead()
    # for i in cur:
    #     print i

