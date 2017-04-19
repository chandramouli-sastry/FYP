import pickle
import pprint
from Resources import mapping, new_fields
import json
import random
import DataServices
from DataServices.Ontology import Ontology
from Misc.rename import shorten

ontology_path="/home/deb/FYP/Resources/ontology.pkl"

def correct(x):
    while x.endswith("_C"):
        x = x[:-2]
    return (x)

with (open(ontology_path, "rb")) as openfile:
    while True:
        try:
            pickle_object = pickle.load(openfile)
        except EOFError:
            break

def filter_func(node):
    return node in mapping.values() or node in new_fields

def get_field_value(tup):
    if len(tup)==2:
        return tup[0]
    else:
        return tup

def generate_json(relationship_dict,index_map_dict):
    #relationship dict tells which node index is related to which other node index
    #index_map_dict maps index to node name
    #var nodes=[{id:0,label:0},{id:1,label:1},{id:2,label:2}]
    #var edges=[{from:0,to:1,id:"e1"},{from:0,to:2,id:"e2"}]

    required_nodes = set()
    edges=[]
    for rel_no in relationship_dict:
        parent=rel_no
        count=0
        required_nodes.add(rel_no)
        for child in relationship_dict[rel_no]:
            temp_dict=dict()
            temp_dict["from"] = rel_no
            temp_dict["to"] = child
            required_nodes.add(child)
            #temp_dict["id"]="e"+str(count)
            count+=1
            edges.append(temp_dict)

    nodes = []
    for index in required_nodes:
        id = index
        label = index_map_dict[index]
        temp_dict = dict()
        temp_dict["label"] = label
        temp_dict["id"] = id
        nodes.append(temp_dict)
    return nodes,edges


def dfs(start,root_count):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            children= set(map(lambda x:correct(x[0]),pickle_object.get_children(correct(vertex))))
            print("For parent ",vertex," Children : ",children)
            print ()
            # new nodes are added to the start of stack
            stack = list(children - visited) + stack
    return visited

#----------------------------------------------------
def main_func():
    nodes = list(filter(filter_func, pickle_object.k2i))
    print ("Total Number of nodes --",len(nodes))
    #***************** find roots ************************************
    # condition for root: hasParent-> False and hasChild->True
    hasParent = {node:False for node in nodes}
    hasChild = {node:False for node in nodes}
    kids = set()
    for node in nodes:
        for child in pickle_object.get_children(node):
            kids.add(correct(child[0]))
            hasParent[correct(child[0])] = True
            hasChild[node] = True

    roots = []
    for node in hasChild:
        if not (hasParent[node]) and hasChild[node]:
            roots.append(node)
    roots_values = len(roots)
    print("Total number of root nodes are - ",roots_values)

    # ***************** connection between main root and roots ************************************

    main_root=-1
    relationship_dict=dict() # tells parent index : [child index1, child index 2...]
    relationship_dict[main_root]=[]
    
    index_map_label_dict=dict() # maps the content : index
    index_map_label_dict['Root']=main_root
    
    root_count=0
    used_set = set() # indicates indices used
    used_set.add(main_root)
    # the relationships formed here dont matter - we wont plot them (redundant code)
    for node in hasChild:
        if not(hasParent[node]) and hasChild[node]:
            roots.append(node)
            index_map_label_dict[node]=root_count
            used_set.add(root_count)
            relationship_dict[main_root].append(root_count)
            root_count+=1

    print("Relationships formed till now -->(Not ncessary) ")
    print(relationship_dict)


    # ***************** Sub Tree Logic ************************************
    graph_json = {}
    root_count=0
    for every_root in roots:
        print("*******************************")
        print ("ROOT --",every_root)
        relationship_dict = {}
        print ("*******************************")
        print(dfs(every_root,root_count))


    """
    #here we shouldnt use the same index again
    graph_json = {}
    for root in roots:
        relationship_dict = {}
        root_index=index_map_label_dict[root]
        children=pickle_object.get_children(root)
        relationship_dict[root_index]=[]
        print ("For Root ",root,"Children are -- ",children)
        print ("************",root_index)
    
        for child in children:
            #get a random index here for the child item
            #root_count=return_randomindex(used_set,roots_values)
            root_count+=1
            print(child,root_count)
            #add this index to used_set
            used_set.add(root_count)
            # add Field : index of field to the dictionary
            index_map_label_dict[get_field_value(child)] = root_count
            #To the parent add the child
            relationship_dict[root_index].append(root_count)
            print (relationship_dict[root_index])
    #print(index_map_label_dict)
        real_index_label = {index_map_label_dict[i]: i for i in index_map_label_dict}
        n,e = generate_json(relationship_dict,real_index_label)
    
        graph_json[root] = {"nodes":n,"edges":e}
    with open("graph.js","w") as f:
        f.write("graph="+json.dumps(graph_json))
    """

main_func()