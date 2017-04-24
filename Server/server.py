from flask import Flask, render_template, request, jsonify
import json
import os
import sqlite3
import pickle
import FactPrinter
from FactPrinter.RatioFactPrinter import RatioFactPrinter
from FactPrinter.SemanticFactPrinterBinary import BinarizedSemanticFactPrinter
from FactPrinter.SimpleFactPrinter import SimpleFactPrinter
from FactPrinter.Writer import Writer

app = Flask(__name__, static_folder='Images', template_folder=".", static_path= '/Images')


def get_metric(fileName):
    obj = json.load(open(fileName))
    if len(obj)>0:
        return max(obj,key=lambda x: x["metric"])["metric"]
    else:
        return -100

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/semantic_list")
def get_semantic():
    list_jsons = os.listdir("../JSONS/Semantic")
    list_names = []
    for name in list_jsons:
        if "Fact_" in name:
            list_names.append((get_metric("../JSONS/Semantic/"+name),name.split("Fact_")[1].replace(".json","")))
    return jsonify(list(map(lambda x:x[1],sorted(list_names,reverse=True))))

@app.route("/semantic_fact")
def get_semantic_fact():
    fact_field = request.args["field"]
    fact_file = "../JSONS/Semantic/Fact_{}.json".format(fact_field)
    fact_json = json.load(open(fact_file))
    writer = Writer(type="list")
    printer = BinarizedSemanticFactPrinter(fact_json,writer=writer)
    printer.process()
    return jsonify(writer.obj)


@app.route("/simple_list")
def get_simple():
    list_jsons = os.listdir("../JSONS/Simple/")
    list_names = []
    for name in list_jsons:
        if "Fact_" in name and name.endswith(".json"):
            list_names.append((get_metric("../JSONS/Simple/"+name),name.split("Fact_")[1].replace(".json","")))
    return jsonify(list(map(lambda x: x[1], sorted(list_names, reverse=True))))

@app.route("/simple_fact")
def get_simple_fact():
    fact_field = request.args["field"]
    fact_file = "../JSONS/Simple/Fact_{}.json".format(fact_field)
    fact_json = json.load(open(fact_file))
    writer = Writer(type="list")
    printer = SimpleFactPrinter(fact_json,writer=writer)
    printer.process()
    return jsonify(writer.obj)

@app.route("/ratio_list")
def get_ratio():
    list_jsons = os.listdir("../JSONS/Ratio")
    list_names = []
    for name in list_jsons:
        if "Fact@" in name:
            list_names.append((get_metric("../JSONS/Ratio/"+name),name.split("Fact@")[1].replace(".json","")))
    return jsonify(list(map(lambda x:x[1],sorted(list_names,reverse=True))))

@app.route("/ratio_fact")
def get_ratio_fact():
    fact_field = request.args["field"]
    fact_file = "../JSONS/Ratio/Fact@{}.json".format(fact_field)
    fact_json = json.load(open(fact_file))
    writer = Writer(type="list")
    printer = RatioFactPrinter(fact_json,writer=writer)
    printer.process()
    return jsonify(writer.obj)



app.run()