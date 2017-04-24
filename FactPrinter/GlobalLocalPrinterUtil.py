from . import identify_dominance, get_fields_to_print
from . import identify_dominance, get_fields_to_print, printer_mapping


class GlobalLocalPrinter:
    def __init__(self,fact_json):
        self.fact_json = fact_json
        self.convertToPercentage("global_perc")
        self.convertToPercentage("local_perc")

    def generateCountSuffixes(self):
        pass

    def extractPercList(self,type):
        partitioned_field_value_list = list()
        perc_list = list()
        for partitioned_field_value in self.fact_json["value_global_local"]:
            partitioned_field_value_list.append(partitioned_field_value)
            perc_list.append(self.fact_json["value_global_local"][partitioned_field_value][type])
        return partitioned_field_value_list,perc_list

    def partition_perc_list(self, field_value_list, perc_list):
        dominance_partitions = identify_dominance(perc_list)
        perc_fields = dict()
        for index, i in enumerate(perc_list):
            for start, end, mean in dominance_partitions:
                if start <= i <= end:
                    perc_fields[mean] = perc_fields.get(mean, list()) + [field_value_list[index]]
                    break
        for perc in perc_fields:
            perc_fields[perc] = sorted(perc_fields[perc], key=lambda x: field_value_list.index(x))

        return perc_fields

    def get_main_content(self,field_name,value):
        if field_name.endswith("_Stat"):
            p = printer_mapping.get(field_name, field_name)
            if p.startswith("Number of"):
                p = p[len("Number of") + 1:].strip()
            p = p + "Status "
            x = value
            x = {'1': 'Available', '2': 'Not Available', '0': 'Not Available'}.get(x, x)
            content = "{} equal to {}.".format(p, x)
        elif field_name.startswith("Dist_"):
            p = printer_mapping.get(field_name, field_name)
            x = value.lower()
            x = {'a': "0-5 KM", 'b': '5-10 KM', 'c': 'more than 10 KM'}.get(x, x)
            content = "{} equal to {}".format(p, x)
        elif field_name.endswith("Gov_1_Priv_2"):
            p = printer_mapping.get(field_name, field_name)
            x = value
            x = {'1': 'Government Facility', '2': 'Private Facility'}.get(x, x)
            content = "{} equal to {}".format(p, x)
        else:
            p = printer_mapping.get(field_name,field_name)
            content = "{} equal to {}.".format(p, value)
        return content

    def generateGlobalSuffix(self):
        global_partitioned_field_values, global_perc_list = self.extractPercList("global_perc")
        global_perc_fields = self.partition_perc_list(global_partitioned_field_values,global_perc_list)

        if len(global_perc_fields)>1:
            if max(global_perc_fields)<5:
                return False

        content = ""
        if len(global_perc_fields) >= 3:
            highest = max(global_perc_fields)
            lowest = min(global_perc_fields)
            s = set(global_perc_fields[highest]) | set(global_perc_fields[lowest])
            medium = (sum(global_perc_list)-highest-lowest)/(len(global_perc_list)-2)
            highest_perc_to_print = highest
            lowest_perc_to_print = lowest
            medium_perc_to_print = medium
            h_fields, h_count = get_fields_to_print(global_perc_fields[highest])
            m_fields, m_count = get_fields_to_print([i for i in global_partitioned_field_values if i not in s])
            l_fields, l_count = get_fields_to_print(global_perc_fields[lowest])
            self.fact_json["partition_field"] = printer_mapping.get(self.fact_json["partition_field"],self.fact_json["partition_field"])
            content = " A whopping {}% of villages having {} equal to {} show this trend,".format(highest_perc_to_print, self.fact_json["partition_field"], h_fields)
            content += " while approximately {}% of villages with {} equal to {} show this trend".format(medium_perc_to_print, self.fact_json["partition_field"], m_fields)
            if lowest != 0:
                content += " and only {}% of villages with {} equal to {} show this trend".format(lowest_perc_to_print, self.fact_json["partition_field"], l_fields)
            content += "."
        elif len(global_perc_fields) == 2:
            highest = max(global_perc_fields)
            lowest = min(global_perc_fields)
            h_fields, h_count = get_fields_to_print(global_perc_fields[highest])
            l_fields, l_count = get_fields_to_print(global_perc_fields[lowest])
            highest_perc_to_print = highest
            lowest_perc_to_print = lowest
            content = "A whopping {}% of villages having {} equal to {} show this trend,".format(highest_perc_to_print,
                                                                                                  self.fact_json[
                                                                                                      "partition_field"],
                                                                                                  h_fields)
            if lowest != 0:
                content += " and only {}% of villages with {} equal to {} show this trend".format(lowest_perc_to_print,
                                                                                                  self.fact_json[
                                                                                                      "partition_field"],
                                                                                                  l_fields)
            content += "."
        elif len(global_perc_fields) == 1:
            # there is only 1 field
            perc = list(global_perc_fields.keys())[0]
            fields, count = get_fields_to_print(global_perc_fields[perc])
            perc_to_print = perc
            content = " approximately {}% of villages with {} equal to {} show this trend.".format(perc, self.fact_json["partition_field"], fields)

        return content

    def generateLocalSuffix(self):
        local_partitioned_field_values, local_perc_list = self.extractPercList("local_perc")

        local_perc_fields = self.partition_perc_list(local_partitioned_field_values, local_perc_list)

        # vil_name, state_name = self.fact_json["Vil_Nam"], self.fact_json["Stat_Nam"]
        # prefix = self.prefix_gen(number) if number != 1 else "{}, a village in {} is one of its kind with ".format(
        #     vil_name, state_name)
        # content = ""
        self.fact_json["partition_field"] = printer_mapping.get(self.fact_json["partition_field"],
                                                                self.fact_json["partition_field"])
        content = ""
        if len(local_perc_fields) >= 3:
            highest = max(local_perc_fields)
            lowest = min(local_perc_fields)
            highest_to_print = highest * len(local_perc_fields[highest])
            lowest_to_print = lowest * len(local_perc_fields[lowest])
            s = set(local_perc_fields[highest]) | set(local_perc_fields[lowest])
            medium = (100 - highest_to_print - lowest_to_print)# / (len(local_perc_list) - 2)
            h_fields, h_count = get_fields_to_print(local_perc_fields[highest])
            m_fields, m_count = get_fields_to_print([i for i in local_partitioned_field_values if i not in s])
            l_fields, l_count = get_fields_to_print(local_perc_fields[lowest])
            content = " A whopping {}% of villages showing this trend have {} equal to {} ,".format(highest_to_print,
                                                                                                  self.fact_json[
                                                                                                      "partition_field"],
                                                                                                  h_fields)
            content += " while approximately {}% of villages showing this trend have {} equal to {}".format(medium,
                                                                                                         self.fact_json[
                                                                                                             "partition_field"],
                                                                                                         m_fields)
            if lowest != 0:
                content += " and only {}% of villages showing this trend have {} equal to {}".format(lowest_to_print,
                                                                                                  self.fact_json[
                                                                                                      "partition_field"],
                                                                                                  l_fields)
            content += "."
        elif len(local_perc_fields) == 2:
            highest = max(local_perc_fields)
            lowest = min(local_perc_fields)
            highest_to_print = highest * len(local_perc_fields[highest])
            lowest_to_print = lowest * len(local_perc_fields[lowest])
            h_fields, h_count = get_fields_to_print(local_perc_fields[highest])
            l_fields, l_count = get_fields_to_print(local_perc_fields[lowest])
            content = " A whopping {}% of villages showing this trend have {} equal to {},".format(highest_to_print,
                                                                                                  self.fact_json[
                                                                                                      "partition_field"],
                                                                                                  h_fields)
            if lowest != 0:
                content += " and only {}% of villages showing this trend have {} equal to {} ".format(lowest_to_print,
                                                                                                  self.fact_json[
                                                                                                      "partition_field"],
                                                                                                  l_fields)
            content += "."
        elif len(local_perc_fields) == 1:
            # there is only 1 field
            perc = list(local_perc_fields.keys())[0]
            fields, count = get_fields_to_print(local_perc_fields[perc])
            avg = sum(local_perc_list) / len(local_perc_list)
            content = " approximately {}% of villages showing this trend have {} equal to {} .".format(avg, self.fact_json[
                "partition_field"], fields)

        return content

    def convertToPercentage(self, type):
        for value in self.fact_json["value_global_local"]:
            self.fact_json["value_global_local"][value][type] *= 100

