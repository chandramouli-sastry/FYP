from DataServices.FunctionGenerators import generateCode
from DataServices.Aggregators import create_sum_function
from DataServices.FileReader import *
from DataServices.Ontology import Ontology
from DataServices.OntologyBuilder import OntologyBuilder
from Resources import mapping
import pickle

# CONFIG
data_file = "Data/full_data.txt"  # The file containing the complete data
data_file = "Data/sample_data.txt"  # The file containing the complete data
indented_factor_file = "Data/Fields_IndentedFactor.txt"  # The indented file for generating factor function calls
indented_aggregate_file = "Data/sample_aggr.txt"  # The indented file for generating aggregate function calls

# Initialize file reader and generate code for building ontology
fileReader = FileReader(data_file,mapping)
print "File Read into memory. "
ontology = Ontology(mapping)
builder = OntologyBuilder(fileReader,ontology)
generateCode(indented_factor_file,indented_aggregate_file)
print "Code Generated. Building Ontology..."
exec(open("code.py").read())
exit()
print "Ontology Built. Pushing to DB.."
builder.buildOntologyandPush(cleanDB=True)
print "DB Populated. Indexing Resources..."

# Update all resources that are needed
with open("Resources/fields.pkl","wb") as f:
    pickle.dump(ontology.fields,f)

with open("Resources/new_fields.pkl","wb") as f:
    pickle.dump(ontology.new_fields,f)

with open("Resources/ontology.pkl","wb") as f:
    pickle.dump(ontology,f)

