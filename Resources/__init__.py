import pickle
mapping = eval(open("Resources/mapping.dict").read())
try:
    fields = pickle.load(open("Resources/fields.pkl"))
    new_fields = pickle.load(open("Resources/new_fields.pkl"))
    ontology = pickle.load(open("Resources/ontology.pkl"))
except Exception as e:
    print "First Time Execution"
    print e