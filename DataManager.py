import csv

import pickle

mapping = eval(open("mapping.dict").read())


class Datum:
    """
    Returns Datum Object which is suitable for doing ...
    """

    def __init__(self, dict):
        for i in dict:
            if mapping[i] != '':
                self.__dict__[mapping[i]] = dict[i]
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
        self.k2i = {}
        i = 0
        for key in map:
            self.k2i[key] = i
            self.k2i[map[key]] = i
            i += 1
        self.matrix = [[0] * len(self.map) for i in range(len(map))]

    def add(self, source, dest, cat):
        self.map[self.k2i[source]][self.k2i[dest]] = (1, cat)
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
            return obj
        except Exception as e:
            print(e)
            return False

    def get_fields(self):
        return self.csvReader.fieldnames


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

    def buildOntologyandPush(self, dataManager):
        while True:
            new_obj = self.fileReader.next_line()
            if new_obj == False:
                break
            datum = Datum(new_obj)
            for new_field, aggregator in self.aggregators:
                datum.__dict__[new_field] = aggregator(datum)
            self.data.append(datum)
        dataManager.writeMultiple(self.data)

    def saveOntology(self, file_name):
        with open("file_name", "wb"):
            pickle.dump(self.ontology)
