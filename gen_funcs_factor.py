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

def print_functions(tree):
    for set in tree:
        for categories in tree[set]:
            category = categories.keys()[0]
            parts = [i.keys()[0] for i in categories.values()[0]]
            for i in categories.values()[0]:
                print_functions(i)
            print "partOf('{}',{},'{}')".format(set,parts,category)

def generate(list_lines):
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

if __name__ == "__main__":
    f=open("Fields_IndentedFactor.txt")
    all_lines = f.readlines()
    lists = extract_contiguous_lists(all_lines)
    for i in lists:
        generate(i)

