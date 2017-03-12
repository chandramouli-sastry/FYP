import pickle
from Properties.Properties import Properties
# l=[4,3,5,1,2]
# Properties(l)

from FactGen.NumericRatioFact import NumericRatioFact

num_fact = NumericRatioFact()
#num_fact.print_facts(number = 30)
num_fact.fuzzy_intersection()
# with open("Resources/fact_pickle.pkl","w") as f:
#     pickle.dump(num_fact,f)

##############################################################
from FactGen.NumericSimpleFact import NumericSimpleFact

num_fact_simple = NumericSimpleFact()
num_fact.fuzzy_intersection()
