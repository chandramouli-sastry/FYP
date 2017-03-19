import pickle
from Properties.Properties import Properties
# l=[4,3,5,1,2]
# Properties(l)

from FactGen.NumericRatioFact import NumericRatioFact
#fact_type = "Ratio"
fact_type = "Statistic"
if fact_type == "Ratio":
    num_fact = NumericRatioFact()
    #num_fact.print_facts(number = 30)
    num_fact.fuzzy_intersection()
    # with open("Resources/fact_pickle.pkl","w") as f:
    #     pickle.dump(num_fact,f)
elif fact_type == "Statistic":
##############################################################
    from FactGen.SimpleStatisticFact import SimpleStatisticFact
    simple = SimpleStatisticFact()
    simple.fuzzy_intersection()
