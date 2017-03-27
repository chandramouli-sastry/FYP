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
            category = list(categories.keys())[0]
            parts = [list(i.keys())[0] for i in list(categories.values())[0]]
            for i in list(categories.values())[0]:
                print_functions_factor(i)
            print(("builder.partOf('{}',{},'{}')".format(set,parts,category)))

def print_function_aggregator(tree):
    """
    TODO: add maxsplit...
    :param tree:
    :return:
    """
    root = list(tree.keys())[0]
    sub_fields_list = list()
    weights_dict = dict()
    maps_dict = dict()
    new_field = root.lstrip().split(' ',4)[1]
    for field_subtree in tree[root]:
        field = list(field_subtree.keys())[0].lstrip()
        sub_fields_list.append(field.split(' ')[1])
        weights_dict[field.split(' ')[1]] = eval(field.split(' ')[0])
        maps_dict[field.split(' ')[1]] = eval(field.split(' ')[3])
        print_function_aggregator(field_subtree)
    if len(tree[root])>0:
        print(("aggregator = create_{}_function({},{},{},'{}')".format(root.split(' ')[2],sub_fields_list,weights_dict,maps_dict,new_field)))
        print(("builder.aggregate('{}',{})".format(new_field,'aggregator')))


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
            while index<len(all_lines) and getLevel(all_lines[index]) != 0:
                list_lines.append(all_lines[index])
                index += 1
            lists.append(list_lines)
        index += 1
    return lists

def generateCode(indented_factor_file,indented_aggregate_file):
    import sys
    code = open("code.py","w")
    sys.stdout = code
    f=open(indented_factor_file)
    all_lines = f.readlines()
    lists = extract_contiguous_lists(all_lines)
    for i in lists:
        generate(i,print_functions_factor)
    g=open(indented_aggregate_file)
    all_lines = g.readlines()
    lists = extract_contiguous_lists(all_lines)
    for i in lists:
        generate(i,print_function_aggregator)
    code.close()
    sys.stdout = sys.__stdout__