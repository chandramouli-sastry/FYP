import random

from FactPrinter.GlobalLocalPrinterUtil import GlobalLocalPrinter
from FactPrinter.QuartileCalculation import quartiles
from fractions import Fraction
from . import num_villages, INF, printer_mapping


class RatioFactPrinter:
    def __init__(self, fact_json, writer):
        self.fact_json = fact_json
        self.writer = writer

    def prefix_gen(self, value):
        quartile1, quartile3 = self.quartiles
        if value == 1:
            return None
        elif value > quartile3:
            return "In a whopping {} number of villages, ".format(value)
        elif value < quartile1:
            return "In only about {} villages, ".format(value)
        else:
            return "In about {} villages, ".format(value)

    def rationalizeRatio(self, ratio):
        _fraction = Fraction.from_float(ratio).limit_denominator(10)
        return _fraction._numerator,_fraction._denominator

    def process(self):
        numbers = [fact["perc"] / 100 * num_villages for fact in self.fact_json]
        if numbers == []:
            return
        self.quartiles = quartiles(numbers)
        for fact in self.fact_json:
            number_of_villages = round(fact["perc"] / 100 * num_villages)
            """
            Prefix: In a whooping {}... | In only about {}... | In about | In {}, a village in {},
            Content: Maximum 3 numbers;
                1. In case, you can find >=3 numbers
                    (The highest) of the Health Facility is predominated by <highest>, with a significant portion of (The Medium) while ...(The Lowest)
                    The medium
                    The lowest
                2. In case, there are only 2 numbers
                    count_highest
                    count_lowest
                    if count_highest>count_lowest:
                        highest_perc of Health is dominated by each of aa, bb among count_highest-2 others, while only cc, dd and count_lowest others constitute just lowest_perc.
                    else:
                        highest_perc of Health is dominated by just aa, bb among count_lowest-2 others, while cc, dd and count_highest others constitute just lowest_perc.
                3. In case, there is only 1 number
                    each of aa, bb and count-2 others have an equal share of Health.
            """
            field1, field2 = printer_mapping.get(fact["data"][1][0],fact["data"][1][0]),printer_mapping.get(fact["data"][0][0],fact["data"][0][0])
            vil_name, state_name = fact["Vil_Nam"], fact["Stat_Nam"]
            prefix = self.prefix_gen(number_of_villages) if number_of_villages != 1 else "{}, a village in {} is one of its kind with ".format(
                vil_name, state_name)
            if fact["data"][2] == INF:
                content = "have {} equal to {} ,".format(fact["data"][1][0], 0)
                content += "with one of them having {} equal to {} and {} equal to {};".format(fact["data"][1][0],fact["data_low"][fact["data"][1][0]],
                                                                                               fact["data"][0][0],fact["data_low"][fact["data"][0][0]])
                content += "while another one of them has {} equal to {} and {} equal to {}.".format(fact["data"][1][0],fact["data_high"][fact["data"][1][0]],
                                                                                               fact["data"][0][0],fact["data_high"][fact["data"][0][0]])
                
            elif fact["data"][2] == INF**2:
                content = "have both {} and {} equal to 0 ".format(fact["data"][0][0], fact["data"][1][0])
            elif fact["perc"]==0:
                content = "have {} equal to {} ,".format(fact["data"][0][0], 0)
                content += "with one of them having {} equal to {} and {} equal to {};".format(fact["data"][1][0],
                                                                                               fact["data_low"][
                                                                                                   fact["data"][1][0]],
                                                                                               fact["data"][0][0],
                                                                                               fact["data_low"][
                                                                                                   fact["data"][0][0]])
                content += "while another one of them has {} equal to {} and {} equal to {}.".format(fact["data"][1][0],
                                                                                                     fact["data_high"][
                                                                                                         fact["data"][
                                                                                                             1][0]],
                                                                                                     fact["data"][0][0],
                                                                                                     fact["data_high"][
                                                                                                         fact["data"][
                                                                                                             1][1]])
            else:
                content = "have ratio between {} and {} equal to {}:{} ".format(fact["data"][0][0], fact["data"][1][0], *self.rationalizeRatio(fact["data"][0][1]/fact["data"][1][1]))
                content += "with one of them having {} equal to {} and {} equal to {};".format(fact["data"][1][0],
                                                                                               fact["data_low"][
                                                                                                   fact["data"][1][0]],
                                                                                               fact["data"][0][0],
                                                                                               fact["data_low"][
                                                                                                   fact["data"][0][0]])
                content += "while another one of them has {} equal to {} and {} equal to {}.".format(fact["data"][1][0],
                                                                                                     fact["data_high"][
                                                                                                         fact["data"][
                                                                                                             1][0]],
                                                                                                     fact["data"][0][0],
                                                                                                     fact["data_high"][
                                                                                                         fact["data"][0][0]])
            if self.writer.type == "list":
                global_local_util = GlobalLocalPrinter(fact)
                self.writer.write([
                    (prefix + content).replace(fact["data"][1][0],field1).replace(fact["data"][1][0],field2),
                    global_local_util.generateLocalSuffix(),
                    global_local_util.generateGlobalSuffix()
                ])
            else:
                self.writer.write(prefix + content)
                self.callGlobalLocal(fact)
