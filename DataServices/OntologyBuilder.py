import pickle

import time

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
            remaining = (set(dependent_fields)-set(self.fields))
            raise Exception("DependencyException : {} not found".format(remaining))
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
        done = False
        while True:
            new_obj = self.fileReader.next_line()
            if new_obj == False:
                break
            datum = Datum(new_obj)
            for new_field, aggregator in self.aggregators:
                result__ = aggregator(datum.__dict__)
                datum.__dict__[new_field] = result__[0]
                for key_ in result__[1]:
                    datum.__dict__[key_ + "_C"] = result__[1][key_]
                datum.__dict__["id"]=count
                if not(done):
                    if len(result__[1])>0:
                        l = self.ontology.tree[self.ontology.k2i[new_field]]
                        for ind,val in enumerate(l):
                            #TODO it keeps appending _C more than once... check...
                            l[ind] = (val[0]+"_C",val[1])
            done = True
            self.data.append(datum)
            count += 1
            if count%10000==0:
                print((str(count)+" done"))
        self.dao.writeMultiple(self.data,cleanDB)

    def saveOntology(self, file_name):
        with open("file_name", "w"):
            pickle.dump(self.ontology)