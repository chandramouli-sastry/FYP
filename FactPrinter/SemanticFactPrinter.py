import random

from FactPrinter.QuartileCalculation import quartiles, median
from . import identify_dominance, num_villages

class SemanticFactPrinter:
    def __init__(self,fact_json,writer):
        self.fact_json = fact_json
        self.writer = writer

    def prefix_gen(self,value):
        quartile1, quartile3 = self.quartiles
        if value == 1:
            return None
        elif value > quartile3:
            return "In a whopping {}".format(value)
        elif value < quartile1:
            return "In only about {}".format(value)
        else:
            return "In about {}".format(value)

    def get_fields_to_print(self,field_list):
        max_fields_to_show = 5
        min_count = 5
        count = len(field_list)
        if (count - max_fields_to_show) > min_count or max_fields_to_show<count:
            to_sample = max_fields_to_show
        else:
            to_sample = count - min_count
        return (", ".join(random.sample(field_list,to_sample)),count-to_sample)


    def process(self):
        numbers = [fact["perc"]*num_villages for fact in self.fact_json]
        self.quartiles = quartiles(numbers)
        for fact in self.fact_json:
            perc_list = map(lambda x:x[1],fact["data"][1])
            number = fact["perc"] * num_villages
            field_list = fact["data"][0][1]
            partitions = identify_dominance(perc_list)
            # {perc:fields}
            perc_fields = {}
            for index,i in enumerate(perc_list):
                for start,end,mean in partitions:
                    if start<=i<=end:
                        perc_fields[mean] = perc_fields.get(mean,[]).append(field_list[index])
                        break
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
            vil_name, state_name = fact["Vil_Nam"],fact["Stat_Nam"]
            prefix = self.prefix_gen(number) if number!=1 else "In {}, a village in {}".format(vil_name,state_name)
            if len(perc_fields)>=3:
                highest = max(perc_fields)
                med = median(perc_fields)
                lowest = min(perc_fields)
                "{} of {} is predominated by {}"
