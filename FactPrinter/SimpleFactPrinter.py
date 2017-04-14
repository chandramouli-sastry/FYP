import random

from FactPrinter.GlobalLocalPrinterUtil import GlobalLocalPrinter
from FactPrinter.QuartileCalculation import quartiles
from . import num_villages


class SimpleFactPrinter:
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

    def process(self):
        numbers = [fact["perc"] / 100 * num_villages for fact in self.fact_json]
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
            vil_name, state_name = fact["Vil_Nam"], fact["Stat_Nam"]
            prefix = self.prefix_gen(number_of_villages) if number_of_villages != 1 else "{}, a village in {} is one of its kind with ".format(
                vil_name, state_name)
            content = "have {} equal to {}.".format(fact["data"][0][0], fact["data"][0][1])
            self.writer.write(prefix + content)
            global_local_util = GlobalLocalPrinter(fact)
            self.writer.write(global_local_util.generateLocalSuffix())
            global_fact = global_local_util.generateGlobalSuffix()
            if global_fact:
                self.writer.write(global_fact)
