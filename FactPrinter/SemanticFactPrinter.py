from . import identify_dominance
class SemanticFactPrinter:
    def __init__(self,fact_json,writer):
        self.fact_json = fact_json
        self.writer = writer
        pass

    def process(self):
        for fact in self.fact_json:
            perc_list = map(lambda x:x[1],fact["data"][1])
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
            Prefix: In a whooping {}... | In only about {}... | In about
            Content: Maximum 3 numbers;
            1. In case, you can find >=3 numbers
                (The highest) of the Health Facility is predominated by <highest>, with a significant portion of (The Medium) while ...(The Lowest)
                The medium
                The lowest
            2. In case, there are only 2 numbers
            3. In case, there is only 1 number
            """