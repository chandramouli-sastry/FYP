from pymongo import MongoClient

class CensusDAO:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.Census
        self.coll = self.db.dataset

    def writeMulitple(self,data):
        for datum in data:
            self.coll.insert_one(datum)

if __name__=="__main__":
    dao = CensusDAO()
    dao.writeMulitple([{"test":"testing"},{"test1":"testing2"}])
    cur = dao.coll.find()
    for i in cur:
        print i

