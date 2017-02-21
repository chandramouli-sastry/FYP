from Graph import Graph
from Resources import mapping
from obtain_listcorrelation import get_correlation

def is_not_related(field1,field2,ontology):
    '''
    Returns true in field1 and field2 are not related in the ontology
    :param field1:
    :param field2:
    :param ontology:
    :return:
    '''
    return not(ontology.is_descendant(field1,field2) or ontology.is_descendant(field2,field1))

def gen_graph(numeric_fields, non_numeric_fields, ontology, datablock):
    g = Graph()
    total_fields = numeric_fields + non_numeric_fields
    for i in total_fields:
        field_list_i = datablock.extract(i)
        if len(set(field_list_i)) == 1:
            continue
        for j in total_fields:
            if j=="" or i=="" or (i,j) in g.graph_ds:
                continue
            field_list_j = datablock.extract(j)
            if len(set(field_list_j)) == 1:
                continue
            if i!=j:
                if is_not_related(i,j,ontology):
                    g.put_value(i,j,value = get_correlation(field_list_i,field_list_j))
    g.compute_top_percentile_graph(10)
    return g


