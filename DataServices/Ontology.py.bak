from Misc.rename import shorten


class Ontology:
    def __init__(self, map):
        """
        Contains Ontology
        :param map: the actual Key to shortened Key mapping
        tree: [list[string] for each of the fields]; the corresponding inner list is the list of children
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
        self.tree[self.k2i[source]].append([dest,cat])
        pass

    def get_descendants(self,ancestor):
        my_children = self.tree[self.k2i[ancestor]]
        my_descendants = []
        for child,cat in my_children:
            my_descendants.extend(self.get_descendants(child))
        return my_children+my_descendants

    def is_descendant(self,ancestor,descendant):
        return descendant in self.get_descendants(ancestor)
