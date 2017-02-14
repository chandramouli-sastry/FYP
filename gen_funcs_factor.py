prev_count = 0
def getLevel(line):
    return len(line) - len(line.lstrip())
d = {}

def make_tree(nodes, parent_level = 0, start_index = 0):
    children = []
    for index in range(start_index+1, len(nodes)):
        (node, node_level) = nodes [index]
        if node_level == parent_level + 1:
            tree_children = make_tree(nodes, node_level,index)
            d = {node: tree_children}
            children.append(d)
        elif node_level <= parent_level:
            break
    if parent_level == 0:
        return {nodes[0][0]:children}
    return children

def print_functions_factor(tree):
    for set in tree:
        for categories in tree[set]:
            category = categories.keys()[0]
            parts = [i.keys()[0] for i in categories.values()[0]]
            for i in categories.values()[0]:
                print_functions_factor(i)
            print "partOf('{}',{},'{}')".format(set,parts,category)

def print_function_aggregator(tree):
    pass


def generate(list_lines,print_functions):
    tuples = [(line,getLevel(line)) for line in list_lines]
    heights = sorted(list(set([i[1] for i in tuples])))
    tuples = [(i[0].strip(), heights.index(i[1])) for i in (tuples)]
    print_functions(make_tree(tuples))

def extract_contiguous_lists(all_lines):
    lists = []
    index = 0
    while index < (len(all_lines)):
        line = all_lines[index]
        if getLevel(line) > 0:
            list_lines = [all_lines[index - 1]]
            while getLevel(all_lines[index]) != 0:
                list_lines.append(all_lines[index])
                index += 1
            lists.append(list_lines)
        index += 1
    return lists



def create_sum_function(dependent_fields,weights, maps, new_field):
    """
        sum aggregate function..
        :param datum: datum object
        :param dependent_fields: list of fields(Strings) on which new field depend on
        :param weights: dictionary of field:weight for every dependent field
        :param maps: dictionary of dictionaries maps[dependentField] = map-->{'a':1,'b':2}
        :param new_field: newField in string
        :return:
    """
    def sum(datum):
        if new_field not in datum:
            datum[new_field] = 0
        for i in dependent_fields:
            if i in maps:
                datum[new_field] += maps[i].get(datum[i],datum[i]) * weights[i]
            else:
                datum[new_field] += weights[i] * datum[i]
        return datum
    sum.dependents=dependent_fields
    return sum


if __name__ == "__main__":
    f=open("Fields_IndentedFactor.txt")
    all_lines = f.readlines()
    lists = extract_contiguous_lists(all_lines)
    for i in lists:
        generate(i,print_functions_factor)

    g=open("Fields_IndentedAggregate.txt")
    all_lines = g.readlines()
    lists = extract_contiguous_lists(all_lines)
    for i in lists:
        generate(i,print_functions_aggregator)
