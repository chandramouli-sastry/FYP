mapping = eval(open("mapping.dict").read())
f = open("Fields_IndentedFactor.txt","wb")
for i in open("fields.txt"):
    toWrite = mapping[i[i.rindex(";")+1:].strip()] if ";" in i else mapping[i.strip()]
    if toWrite!="":
        f.write(toWrite.strip("\n")+"\n")
