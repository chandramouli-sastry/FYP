import pickle
class DataBlock:
    def __init__(self,_list, name):
        self.list_dicts = _list
        self.name = name

    def extract(self, field_name):
        values = [i[field_name] for i in self.list_dicts]
        return values

    def save(self):
        with open(self.name,"wb") as f:
            pickle.dump(self,f)
