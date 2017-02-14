'''f = open("fields.txt")
l = f.readlines()
fields = ""
count = 0
for i in l:
    count +=1
    if ";" in i:
        ind = i.rindex(";")
        field = i[ind+1:].strip()
        if "," in field:
            fields += "\\\""+field+"\\\""
        else:
            fields += field
    else:
        fields += i.strip()
    #if "," in i:
        #print i
    fields += ","
print count
print fields
'''
import pprint
import csv

# pprint.pprint(line[:50])
# pprint.pprint(len(line))

import re
pat = re.compile("\w+")
word_re = re.compile("[aeiou].*?[^aeiou]")
alt1 = re.compile("[^aeiou]")
alt2 = re.compile(".*")
def shorten(field_name):
    def trim(word):
        try:
            return word[0]+word[1:(word_re.search(word[1:]) or alt1.search(word[1:])  or alt2.search(word[1:])).span()[1]+1]
        except Exception as e:
            print word
            exit(-1)
    list_words = pat.findall(field_name)
    list_words = map(trim,list_words)
    return "_".join(list_words)

if __name__ == "__main__":
    f = open("/Users/cshamasastry/Documents/Spl Topic/Interestingness/input1.txt")
    f = csv.reader(f)
    line = next(f)
    d = {}
    for i in line:
        d[i] = shorten(i)
    print len(d)
    with open("mapping.dict","wb") as f:
        pprint.pprint(d,f)

