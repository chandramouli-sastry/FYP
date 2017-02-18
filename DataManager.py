import csv

import pickle

from DAO import CensusDAO
from rename import shorten
mapping = eval(open("mapping.dict").read())


class Datum:
    """
    Returns Datum Object which is suitable for doing ...
    """

    def __init__(self, dict):
        for i in dict:
            self.__dict__[i] = dict[i]
        pass

class DataManager:
    def __init__(self, ontology, source, dbPath):
        pass

    def writeMultiple(self, list_data):
        pass

    def updateDB(self, selector, clean=False):
        pass

    def query(self, queryParams):
        pass

    def read(self, generator=True):
        pass


class Ontology:
    def __init__(self, map):
        """
        Contains Ontology
        :param map: the actual Key to shortened Key mapping
        """
        self.k2i = {}
        i = 0
        for key in map:
            self.k2i[key] = i
            self.k2i[map[key]] = i
            i += 1
        self.tree = [[] for i in range(len(map))]

    def new_field(self,new_field):
        self.k2i[new_field] = len(self.tree)
        self.k2i[shorten(new_field)] = len(self.tree)
        self.tree.append([])

    def add(self, source, dest, cat):
        self.tree[self.k2i[source]].append([self.k2i[dest],cat])
        pass


class FileReader:
    def __init__(self, file_name):
        self.csvReader = csv.DictReader(open(file_name))

    def isValid(self, obj):
        for i in obj:
            if obj[i] == i:
                return False
        return True

    def next_line(self):
        try:
            obj = next(self.csvReader)
            while not (self.isValid(obj)):
                obj = next(self.csvReader)
            obj = {mapping[i]:obj[i] for i in obj if mapping[i]!=''}
            return obj
        except Exception as e:
            print(e)
            return False

    def get_fields(self):
        return [mapping[i] for i in self.csvReader.fieldnames if mapping[i]!='']


class OntologyBuilder:
    def __init__(self, fileReader, ontology):
        '''
        :param file_name: Reads first line and interprets them as the fields
        '''
        self.aggregators = []
        self.fileReader = fileReader
        self.fields = fileReader.get_fields()
        self.ontology = ontology
        self.data = []
        self.dao = CensusDAO()
        pass

    def aggregate(self, new_field, compute_function):
        """
        Used for adding summary type fields.
        :param new_field: creates new_field for every datum;
        :param compute_function: compute_function takes in datum and returns the new_field. compute_function should have a property called dependents which must list all the dependent fields
        :raises DependencyException if dependent fields arent yet available.
        calls partOf while returning.
        :return:
        """
        dependent_fields = set(compute_function.dependents)
        if not (dependent_fields < set(self.fields)):
            raise Exception("DependencyException")
        self.fields.append(new_field)
        self.aggregators.append([new_field, compute_function])
        self.ontology.new_field(new_field)
        self.partOf(new_field, list(dependent_fields), "subclass")

    def partOf(self, whole, parts, category):
        """
        Used for adding "part-of" relationships
        :param whole:
        :param parts:
        :return:
        """
        for part in parts:
            self.ontology.add(whole, part, category)

    def buildOntologyandPush(self):
        while True:
            new_obj = self.fileReader.next_line()
            if new_obj == False:
                break
            datum = Datum(new_obj)
            for new_field, aggregator in self.aggregators:
                datum.__dict__[new_field] = aggregator(datum.__dict__)
            self.data.append(datum)
        self.dao.writeMultiple(self.data)

    def saveOntology(self, file_name):
        with open("file_name", "wb"):
            pickle.dump(self.ontology)
