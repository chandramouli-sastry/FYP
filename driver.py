from DataManager import *
from gen_funcs_factor import create_sum_function
fileReader = FileReader("sample_inp.txt")
ontology = Ontology(mapping)
builder = OntologyBuilder(fileReader,ontology)
builder.partOf('Tot_Pop_of_Vil',['Tot_Mal_Pop_of_Vil', 'Tot_Fem_Pop_of_Vil'],'Gender')
builder.partOf('Tot_Sched_Cas_Pop_of_Vil',['Tot_Sched_Cas_Mal_Pop_of_Vil', 'Tot_Sched_Cas_Fem_Pop_of_Vil'],'Gender')
builder.partOf('Tot_Sched_Trib_Pop_of_Vil',['Tot_Sched_Trib_Mal_Pop_of_Vil', 'Tot_Sched_Trib_Fem_Pop_of_Vil'],'Gender')
builder.partOf('Tot_Pop_of_Vil',['Tot_Sched_Cas_Pop_of_Vil', 'Tot_Sched_Trib_Pop_of_Vil'],'Caste')
aggregator = create_sum_function(['Gov_Prim_School_Num', 'Priv_Prim_School_Num', 'Near_Prim_School_Gov_1_Priv_2', 'Dist_Prim_School'],{'Priv_Prim_School_Num': 0.4, 'Gov_Prim_School_Num': 0.6, 'Dist_Prim_School': 0.5, 'Near_Prim_School_Gov_1_Priv_2': 0.5},{'Priv_Prim_School_Num': {'': 0, 'N.A.': 0}, 'Gov_Prim_School_Num': {'': 0, 'N.A.': 0}, 'Dist_Prim_School': {'A': 3, '': 0, 'C': 1, 'B': 2, 'N.A.': 0}, 'Near_Prim_School_Gov_1_Priv_2': {'1': 2, '': 0, '2': 1, 'N.A.': 0}},'Primary_School')
builder.aggregate('Primary_School',aggregator)
builder.buildOntologyandPush()