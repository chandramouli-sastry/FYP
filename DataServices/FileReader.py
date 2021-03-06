import codecs
import csv
import re
# class DataManager:
#     def __init__(self, ontology, source, dbPath):
#         pass
#
#     def writeMultiple(self, list_data):
#         pass
#
#     def updateDB(self, selector, clean=False):
#         pass
#
#     def query(self, queryParams):
#         pass
#
#     def read(self, generator=True):
#         pass


class FileReader:
    def __init__(self, file_name, mapping):
        self.file = codecs.open(file_name,"r",encoding="latin-1")
        self.lines = list(csv.reader(self.file))
        self.fields = self.lines.pop(0)
        self.full_fields = self.fields
        self.csvReader = iter(self.lines)
        self.mapping = mapping
        self.fields = [self.mapping[i] for i in self.fields]
        #self.print_string_values()

    def eval_lists(self):
        pass

    def isValid(self, line):
        return len(set(line)&set(self.full_fields))==0

    def next_line(self):
        try:
            line = next(self.csvReader)
            while not (self.isValid(line)):
                line = next(self.csvReader)
            obj = {key:value.strip() for key,value in zip(self.fields,line) if key!=''}
            return obj
        except Exception as e:
            print(e)
            return False

    def print_string_values(self):
        sets = [set() for i in range(len(self.fields))]
        pat = re.compile("[A-Za-z0-9]")
        for line in self.lines:
            for index in range(len(self.fields)):
                if self.fields[index] == "":
                    continue
                if pat.search(line[index]):
                    sets[index] |= set([line[index]])

        for index,_set in enumerate(sets):
            if len(_set) <= 10:
                print((self.fields[index]))
                for value in _set:
                    print(("\t"+value))

    def get_fields(self):
        return [i for i in self.fields if i!='']