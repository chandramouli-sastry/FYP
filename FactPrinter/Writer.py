import sys
class Writer:
    def __init__(self,type):
        self.type = type
        if type=="file":
            self.obj = open("Out.txt","w")
        elif type=="list":
            self.obj = []
        elif type == "sout":
            self.obj = None

    def write(self,string):
        if self.type == "list":
            self.obj.append(string)
        elif self.type == "file":
            self.obj.write(string+"\n")
        elif self.type == "sout":
            print(string)
