import pickle
mapping = eval(open("Resources/mapping.dict").read())
convert = lambda x: 0 if x.strip()=="" else float(x)

try:
    fields = pickle.load(open("Resources/fields.pkl","rb"))
    if "Dist_PI_Cod" in fields:
        fields.remove("Dist_PI_Cod")
    if "" in fields:
        fields.remove("")
    new_fields = pickle.load(open("Resources/new_fields.pkl","rb"))
    numeric_fields = pickle.load(open("Resources/numeric_fields.pkl","rb"))
    non_numeric_fields = pickle.load(open("Resources/non_numeric_fields.pkl","rb"))
    continuous_fields = pickle.load(open("Resources/continuous_fields.pkl","rb"))
    discrete_fields = pickle.load(open("Resources/discrete_fields.pkl","rb"))
    ontology = pickle.load(open("Resources/ontology.pkl","rb"))
except Exception as e:
    print ("First Time Execution")
    print (e)
