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
        if relationship_dict[rel_no]:
            for child in relationship_dict[rel_no]:
                temp_dict=dict()
                temp_dict["from"] = rel_no
                temp_dict["to"] = child
                required_nodes.add(child)
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

def map_parents_to_children(parent,children_set,index_map_label_dict,relationship_dict):
    parent_index = index_map_label_dict[parent]
    relationship_dict[parent_index] = []
    if children_set:
        #only if this set isnt empty
        for child in children_set:
            child_index=index_map_label_dict[child]
            relationship_dict[parent_index].append(child_index)
    return relationship_dict


def retrieve_relationships(start,index_map_label_dict,relationship_dict):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            children= set(map(lambda x:correct(x[0]),pickle_object.get_children(correct(vertex))))
            #update relationships between parent and its children
            relationship_dict=map_parents_to_children(vertex,children,index_map_label_dict,relationship_dict)
            print("Mapping parent ", vertex, " to Children : ", children)
            # new nodes are added to the start of stack
            stack = list(children - visited) + stack
    return relationship_dict

def retrieve_connections(start,root_count,used_set,index_map_label_dict):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            root_count+=1
            #Update the dictionary which maps nodes to their indexes
            index_map_label_dict[vertex] = root_count
            print("Vertex --> ",vertex,"--",root_count)
            used_set.add(root_count)
            visited.add(vertex)
            children= set(map(lambda x:correct(x[0]),pickle_object.get_children(correct(vertex))))
            # new nodes are added to the start of stack
            stack = list(children - visited) + stack
    return root_count

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

    used_set = set()

    relationship_dict=dict() # tells parent index : [child index1, child index 2...]

    index_map_label_dict=dict() # maps the content : index

    for node in hasChild:
        if not(hasParent[node]) and hasChild[node]:
            roots.append(node)

    # ***************** Sub Tree Logic ************************************
    graph_json = {}
    root_count=0
    graph_json={}
    for every_root in roots:
        print("*******************************")
        print ("ROOT --",every_root)
        relationship_dict = {}
        print ("*******************************")
        #establish connections
        root_count=retrieve_connections(every_root,root_count,used_set,index_map_label_dict)
        relationship_dict=retrieve_relationships(every_root,index_map_label_dict,relationship_dict)
        """
        print("Relationship dict modified")
        for key in relationship_dict:
            print(key, relationship_dict[key])
        print()
        """
        real_index_label = {index_map_label_dict[i]: i for i in index_map_label_dict}
        n, e = generate_json(relationship_dict, real_index_label)
        graph_json[every_root] = {"nodes": n, "edges": e}
        with open("graph.js", "w") as f:
            f.write("graph=" + json.dumps(graph_json))
        print ("Graph.js written!")

main_func()