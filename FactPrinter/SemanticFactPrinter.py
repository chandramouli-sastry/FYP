import random

from FactPrinter.QuartileCalculation import quartiles, median
from . import identify_dominance, num_villages, get_fields_to_print

class SemanticFactPrinter:
    def __init__(self,fact_json,writer):
        self.fact_json = fact_json
        self.writer = writer

    def prefix_gen(self,value):
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
        numbers = [fact["perc"]/100*num_villages for fact in self.fact_json]
        self.quartiles = quartiles(numbers)
        for fact in self.fact_json:
            number = round(fact["perc"]/100 * num_villages)
            field_list = fact["data"][0][1]
            perc_list = list(map(lambda field: fact["data"][1][field], field_list))
            partitions = identify_dominance(perc_list)
            # {perc:fields}
            perc_fields = {}
            for index,i in enumerate(perc_list):
                for start,end,mean in partitions:
                    if start<=i<=end:
                        perc_fields[mean] = perc_fields.get(mean,[]) + [field_list[index]]
                        break
            for perc in perc_fields:
                perc_fields[perc] = sorted(perc_fields[perc],key = lambda x:field_list.index(x))
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
            prefix = self.prefix_gen(number) if number!=1 else "{}, a village in {} is one of its kind with ".format(vil_name,state_name)
            content = ""
            if len(perc_fields)>=3:
                highest = max(perc_fields)
                lowest = min(perc_fields)
                s = set(perc_fields[highest])|set(perc_fields[lowest])
                h_fields,h_count = get_fields_to_print(perc_fields[highest])
                m_fields,m_count = get_fields_to_print([i for i in field_list if i not in s])
                l_fields,l_count = get_fields_to_print(perc_fields[lowest])
                if lowest!=0:
                    content = "{} and {} others predominate {} with each constituting {}%, while {} and {} others each constitute just {}% with a considerable share by {} and {} others.".format(
                        h_fields,h_count,
                        fact["data"][0][0],highest,
                        l_fields,l_count,lowest,
                        m_fields,m_count
                    )
                else:
                    content = "{} and {} others predominate {} with each constituting {}%, while {} and {} others have zero share, with {} and {} others constituting the remaining.".format(
                        h_fields, h_count,
                        fact["data"][0][0], highest,
                        l_fields, l_count,
                        m_fields, m_count
                    )
            elif len(perc_fields) == 2:
                highest = max(perc_fields)
                lowest = min(perc_fields)
                h_fields, h_count = get_fields_to_print(perc_fields[highest])
                l_fields, l_count = get_fields_to_print(perc_fields[lowest])
                if lowest!=0:
                    content = "{} and {} others predominate {} with each constituting {}%, while {} and {} others each constitute just {}%.".format(
                        h_fields, h_count,
                        fact["data"][0][0], highest,
                        l_fields, l_count, lowest
                    )
                else:
                    content = "{} and {} others predominate {} with each constituting {}%, while {} and {} others have zero share.".format(
                        h_fields, h_count,
                        fact["data"][0][0], highest,
                        l_fields, l_count
                    )
            elif len(perc_fields)==1:
                # there is only 1 field
                perc = list(perc_fields.keys())[0]
                fields, count = get_fields_to_print(perc_fields[perc])
                content = "{} and {} others equally constitute {}.".format(
                    fields, count,
                        fact["data"][0][0]
                    )
            self.writer.write(prefix+content)