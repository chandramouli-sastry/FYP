import pickle

from DataServices import Datum
from DataServices.DBController import CensusDB


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
        self.dao = CensusDB()
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

    def buildOntologyandPush(self,cleanDB=False):
        count = 0
        while True:
            new_obj = self.fileReader.next_line()
            if new_obj == False:
                break
            datum = Datum(new_obj)
            for new_field, aggregator in self.aggregators:
                datum.__dict__[new_field] = aggregator(datum.__dict__)
            self.data.append(datum)
            count += 1
            if count%10000==0:
                print str(count)+" done"
        self.dao.writeMultiple(self.data,cleanDB)

    def saveOntology(self, file_name):
        with open("file_name", "wb"):
            pickle.dump(self.ontology)