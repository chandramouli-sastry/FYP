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
        f=open("DEBUG.log","wb")
        f.write(str({i:datum[i] for i in dependent_fields}))
        f.close()
        SUM = 0
        for i in dependent_fields:
            if i in maps:
                SUM += float(maps[i].get(datum[i],datum[i])) * weights[i]
            else:
                SUM += weights[i] * eval(datum[i])
        return SUM
    sum.dependents=dependent_fields
    return sum