class Datum:
    """
    Returns Datum Object which is suitable for doing ...
    """
    def __init__(self,dict):
        pass


class DataManager:
    def __init__(self, ontology, source, dbPath):
        pass

    def updateDB(self,selector,clean=False):
        pass

    def query(self,queryParams):
        pass

    def read(self,generator=True):
        pass


class Ontology:
    def __init__(self, map ):
        self.k2i = {}
        i = 0
        for key in map:
            self.k2i[key] = i
            self.k2i[map[key]] = i
            i += 1
        self.matrix = [[0]*len(self.map) for i in range(len(map))]




    def add(self, source, dest):
        self.map[self.k2i[source]][self.k2i[dest]] = 1
        pass

class OntologyBuilder:
    def __init__(self,file_name):
        '''
        :param file_name: Reads first line and interprets them as the fields
        '''
        aggregators = []
        dag = []
        pass

    def aggregate(self,new_field,compute_function):
        """
        Used for adding summary type fields.
        :param new_field: creates new_field for every datum;
        :param compute_function: compute_function takes in datum and returns the new_field. compute_function should have a property called dependents which must list all the dependent fields
        :raises DependencyException if dependent fields arent yet available.
        calls partOf while returning.
        :return:
        """
        pass

    def partOf(self,whole,part,category):
        """
        Used for adding "part-of" relationships
        :param whole:
        :param part:
        :return:
        """
        pass

    def finalize(self):
        for datum in self.data:
            for new_field,aggregator in self.aggregators:
                datum.__dict__[new_field] = aggregator(datum)
