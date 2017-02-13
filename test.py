def decorator(func,l):
    def temp(*args,**kwargs):
        func(*args,**kwargs)
    temp.l=l
    return temp

def easy():
    print l

x=[decorator(easy,['a','b']),decorator(easy,['1','2'])]

x[0]()
x[1]()