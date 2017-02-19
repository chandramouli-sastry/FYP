from Misc.rename import shorten


class Ontology:
    def __init__(self, map):
        """
        Contains Ontology
        :param map: the actual Key to shortened Key mapping
        """
        self.k2i = {}
        self.fields = map.values()
        self.new_fields = []
        i = 0
        for key in map:
            self.k2i[key] = i
            self.k2i[map[key]] = i
            i += 1
        self.tree = [[] for i in range(len(map))]

    def new_field(self,new_field):
        self.k2i[new_field] = len(self.tree)
        self.k2i[shorten(new_field)] = len(self.tree)
        self.new_fields.append(new_field)
        self.tree.append([])

    def add(self, source, dest, cat):
        self.tree[self.k2i[source]].append([self.k2i[dest],cat])
        pass
