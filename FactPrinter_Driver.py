# from FactPrinter.NumericRatioFactPrinter import run_test
#
# run_test()
import json

from FactPrinter.SemanticFactPrinter import SemanticFactPrinter
from FactPrinter.Writer import Writer

fact_json = json.load(open("Resources/Facts_data_Semantic_Education.json"))
#fact_json = json.load(open("Resources/Facts_data_Semantic_Health.json"))
writer = Writer("sout")
printer = SemanticFactPrinter(fact_json,writer)
printer.process()