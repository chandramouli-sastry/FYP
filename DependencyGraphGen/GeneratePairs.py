from Graph import Graph
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


def gen_graph(fields, new_fields, ontology, datablock):
    g = Graph()
    total_fields = fields+new_fields
    for i in total_fields:
        for j in total_fields:
            if i!=j:
                if is_not_related(i,j,ontology):
                    g.put_value(i,j,get_correlation(datablock.extract(i),datablock.extract(j)))
    g.compute_top_percentile_graph(10)
    return g


