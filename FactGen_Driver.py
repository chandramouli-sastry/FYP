import pickle

from FactGen.NumericRatioFact import NumericRatioFact

num_fact = NumericRatioFact()
#num_fact.print_facts(number = 30)
with open("Resources/fact_pickle.pkl","wb") as f:
    pickle.dump(num_fact,f)