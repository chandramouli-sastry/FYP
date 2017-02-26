import pickle
from multiprocessing import Pool


class DataBlock:
    def __init__(self,_list, name):
        self.list_dicts = _list
        self.name = name

    def extract(self, field_name):
        try:
            values = [i[field_name] for i in self.list_dicts]
        except Exception as e:
            print e
            print i
        return values

    def apply(self,function):
        p = Pool(5)
        ret_list = p.map(function,self.list_dicts)
        p.close()
        return ret_list

    def save(self):
        with open(self.name,"wb") as f:
            pickle.dump(self,f)
