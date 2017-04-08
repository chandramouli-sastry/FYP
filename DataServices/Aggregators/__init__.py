def convert(x):
    if type(x)==type("") and x.strip()=="":
        return 0
    else:
        try:
            return float(x)
        except:
            return 0

def create_sum_function(dependent_fields,weights, maps, new_field):
    """
        sum aggregate function..
        :param datum: datum object
        :param dependent_fields: list of fields(Strings) on which new field depend on
        :param weights: dictionary of field:weight for every dependent field
        :param maps: dictionary of dictionaries maps[dependentField] = map-->{'a':1,'b':2}
        :param new_field: newField in string
        :return:
    """
    def sum(datum):
        # f=open("DEBUG.log","w")
        # f.write(str({i:datum[i] for i in dependent_fields}))
        # f.close()
        SUM = 0
        values = {}
        should_change = False
        for i in dependent_fields:
            if i in maps:
                maps[i][""] = 0
                values[i] = convert(maps[i].get(datum[i], datum[i]))
                should_change = True
            else:
                values[i] = eval(datum[i])
            SUM += weights[i] * values[i]
        if should_change:
            return SUM,values
        else:
            return SUM,[]
    sum.dependents=dependent_fields
    return sum