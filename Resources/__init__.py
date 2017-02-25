import pickle
mapping = eval(open("Resources/mapping.dict").read())
convert = lambda x: 0 if x=="" else float(x)

try:
    fields = pickle.load(open("Resources/fields.pkl"))
    if "Dist_PI_Cod" in fields:
        fields.remove("Dist_PI_Cod")
    if "" in fields:
        fields.remove("")
    new_fields = pickle.load(open("Resources/new_fields.pkl"))
    numeric_fields = pickle.load(open("Resources/numeric_fields.pkl"))
    non_numeric_fields = pickle.load(open("Resources/non_numeric_fields.pkl"))
    continuous_fields = pickle.load(open("Resources/continuous_fields.pkl"))
    discrete_fields = pickle.load(open("Resources/discrete_fields.pkl"))
    ontology = pickle.load(open("Resources/ontology.pkl"))
except Exception as e:
    print "First Time Execution"
    print e