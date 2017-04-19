import random

from FactPrinter.GlobalLocalPrinterUtil import GlobalLocalPrinter
from FactPrinter.QuartileCalculation import quartiles
from . import num_villages, get_fields_to_print, printer_mapping


class SimpleFactPrinter:
    def __init__(self, fact_json, writer):
        self.fact_json = fact_json
        self.writer = writer

    def prefix_gen(self, value):
        quartile1, quartile3 = self.quartiles
        if value == 1:
            return None
        elif value > quartile3:
            return "a whopping {} number of villages ".format(value)
        elif value < quartile1:
            return "only about {} villages ".format(value)
        else:
            return "about {} villages ".format(value)

    def process(self):
        numbers = [fact["perc"] / 100 * num_villages for fact in self.fact_json]
        if len(numbers)>1:
            self.quartiles = quartiles(numbers)
        else:
            self.quartiles = numbers[0], numbers[-1]

        for fact in self.fact_json:
            if fact["internal"]:
                self.binarizedProcess(fact)
            number_of_villages = round(fact["perc"] / 100 * num_villages)
            vil_name, state_name = fact["Vil_Nam"], fact["Stat_Nam"]
            prefix = self.prefix_gen(number_of_villages) if number_of_villages != 1 else "{}, a village in {} is one of its kind having".format(
                vil_name, state_name)
            if fact["data"][0][0].endswith("_Stat"):
                p = printer_mapping.get(fact["data"][0][0],fact["data"][0][0])
                if p.startswith("Number of"):
                    p = p[len("Number of")+1:].strip()
                x = fact["data"][0][1]
                x = {'1':'Available','2':'Not Available','0':'Not Available'}.get(x,x)
                prefix = "In "+ prefix
                content = ", {} is {}.".format(p, x)
            elif fact["data"][0][0].startswith("Dist_") :
                p = printer_mapping.get(fact["data"][0][0], fact["data"][0][0])
                x = fact["data"][0][1].lower()
                x = {'a':"0-5 KM", 'b': '5-10 KM', 'c': 'more than 10 KM'}.get(x,x)
                prefix = "In " + prefix
                content = ", {} is {}.".format(p, x)
            elif fact["data"][0][0].endswith("Gov_1_Priv_2"):
                p = printer_mapping.get(fact["data"][0][0], fact["data"][0][0])
                x = fact["data"][0][1]
                x = {'1': 'Government Facility', '2': 'Private Facility'}.get(x, x)
                prefix = "In " + prefix
                content = ", {} is {}.".format(p, x)
            else:
                p = printer_mapping.get(fact["data"][0][0], fact["data"][0][0])
                prefix = prefix[0].upper() + prefix[1:]
                content = "{}{} equal to {}.".format( "have " if number_of_villages!=1 else "",p, fact["data"][0][1])
            if self.writer.type == "list":
                global_local_util = GlobalLocalPrinter(fact)
                self.writer.write([fact["metric"],
                    prefix + content,
                    global_local_util.generateLocalSuffix(),
                    global_local_util.generateGlobalSuffix()
                ])
            else:
                self.writer.write(prefix + content)
                self.callGlobalLocal(fact)

    def binarizedProcess(self, fact):
        numbers = [fact["perc"] / 100 * num_villages for fact in self.fact_json]
        self.quartiles = quartiles(numbers)
        number_of_villages = round(fact["perc"] / 100 * num_villages)
        vil_name, state_name = fact["Vil_Nam"], fact["Stat_Nam"]
        if number_of_villages!=1:
            prefix = self.prefix_gen(number_of_villages)
            if fact["data"][1] == "have":
                content = "have {}.".format(fact["data"][0])
            else:
                content = "do not have {}.".format(fact["data"][0])
        else:
            prefix = "{}, a village in {} is one of its kind, ".format(
                vil_name, state_name)
            if fact["data"][1] == "have":
                content = "because it has {}.".format(fact["data"][0])
            else:
                content = "because it does not have {}.".format(fact["data"][0])
        if self.writer.type == "list":
            global_local_util = GlobalLocalPrinter(fact)
            self.writer.write([fact["metric"],
                prefix+content,
                global_local_util.generateLocalSuffix(),
                global_local_util.generateGlobalSuffix()
            ])
        else:
            self.writer.write(prefix + content)
            self.callGlobalLocal(fact)

    def callGlobalLocal(self, fact):
        global_local_util = GlobalLocalPrinter(fact)
        self.writer.write(global_local_util.generateLocalSuffix())
        global_fact = global_local_util.generateGlobalSuffix()
        if global_fact:
            self.writer.write(global_fact)