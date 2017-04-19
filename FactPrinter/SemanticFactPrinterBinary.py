import random

from FactPrinter.GlobalLocalPrinterUtil import GlobalLocalPrinter
from FactPrinter.QuartileCalculation import quartiles, median
from . import identify_dominance, num_villages, get_fields_to_print

'''
{"have":[list...], "have-not":[list...], global_local_dict:{}, perc:, count: }
'''

class BinarizedSemanticFactPrinter:
    def __init__(self, fact_json, writer):
        self.fact_json = fact_json
        self.writer = writer

    def prefix_gen(self, value):
        quartile1, quartile3 = self.quartiles
        if value == 1:
            return None
        elif value > quartile3:
            return "A whopping {} number of villages ".format(value)
        elif value < quartile1:
            return "Only about {} villages ".format(value)
        else:
            return "About {} villages ".format(value)

    def generateListOfFieldsContent(self,fields,count):
        content = fields
        if count > 0:
            content += " and {} others".format(count)
        return content

    def process(self):
        numbers = [fact["perc"] / 100 * num_villages for fact in self.fact_json]
        self.quartiles = quartiles(numbers)
        for fact in self.fact_json:
            # perc_list = list(map(lambda x: x[1], fact["data"][1]))
            number = round(fact["perc"] / 100 * num_villages)
            # field_list = fact["data"][0][1]
            # partitions = identify_dominance(perc_list)
            # # {perc:fields}
            # perc_fields = {}
            # for index, i in enumerate(perc_list):
            #     for start, end, mean in partitions:
            #         if start <= i <= end:
            #             perc_fields[mean] = perc_fields.get(mean, []) + [field_list[index]]
            #             break
            # for perc in perc_fields:
            #     perc_fields[perc] = sorted(perc_fields[perc], key=lambda x: field_list.index(x))
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
            vil_name, state_name = fact["Vil_Nam"], fact["Stat_Nam"]
            if number != 1:
                prefix = self.prefix_gen(number)
                content = "have {} ".format(self.generateListOfFieldsContent(*get_fields_to_print(fact["have"], binarize=True))) if fact["have"] else ""
                content += " and " if fact["have"] and fact["have_not"] else " "
                content += " do not have {}.".format(self.generateListOfFieldsContent(*get_fields_to_print(fact["have_not"], binarize=True))) if fact["have_not"] else ""
            else:
                prefix = "{}, a village in {} is one of its kind which  ".format(vil_name, state_name)
                content = "has {}".format(
                    self.generateListOfFieldsContent(*get_fields_to_print(fact["have"], binarize=True))) if fact["have"] else ""
                content += " and " if fact["have"] and fact["have_not"] else " "
                content += " does not have {}.".format(
                    self.generateListOfFieldsContent(*get_fields_to_print(fact["have_not"], binarize=True))) if fact["have_not"] else ""

            if self.writer.type == "list":
                global_local_util = GlobalLocalPrinter(fact)
                self.writer.write([
                    prefix + content,
                    global_local_util.generateLocalSuffix(),
                    global_local_util.generateGlobalSuffix()
                ])
            else:
                self.writer.write(prefix + content)
                self.callGlobalLocal(fact)
