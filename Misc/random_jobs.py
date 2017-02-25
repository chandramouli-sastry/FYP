# mapping = eval(open("mapping.dict").read())
# f = open("Fields_IndentedFactor.txt","wb")
# for i in open("fields.txt"):
#     toWrite = mapping[i[i.rindex(";")+1:].strip()] if ";" in i else mapping[i.strip()]
#     if toWrite!="":
#         f.write(toWrite.strip("\n")+"\n")
# from Resources import fields,new_fields
import pickle
# convert = lambda x: 0 if x=="" else float(x)
#
# datablock = pickle.load(open("Resources/sample_100.pkl"))
# def numeric_fields():
#     numeric_list = []
#     non_numeric_list = []
#     for field_name in fields:
#         if field_name=="":continue
#         list_values = datablock.extract(field_name)
#         try:
#             x = map(convert,list_values)
#             if len(set(x)-set([0])) > 0:
#                 numeric_list.append(field_name)
#         except ValueError:
#             non_numeric_list.append(field_name)
#     with open("Resources/numeric_fields.pkl","wb") as f:
#         pickle.dump(numeric_list,f)
#     with open("Resources/non_numeric_fields.pkl","wb") as f:
#         pickle.dump(non_numeric_list,f)

def continuous_fields():
    continuous_list = []
    discrete_list = []
    f = open("../Data/Fields_Type")
    for line in f:
        try:
            line,type = line.strip().split()
        except Exception as e:
            print "here",e,line
        if type.lower()=="c":
            continuous_list.append(line.strip())
        else:
            discrete_list.append(line.strip())
    with open("../Resources/continuous_fields.pkl","wb") as f:
        pickle.dump(continuous_list,f)
    with open("../Resources/discrete_fields.pkl","wb") as f:
        pickle.dump(discrete_list,f)

continuous_fields()
