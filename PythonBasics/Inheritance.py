######
# Classes
######

# Note: "self" in python has similar meaning to "this" in java 
class myClass:
    oneval = 17
    def div(self, int_in):
        return int_in / self.oneval
    #Python Constructor
    def __init__(self, inval):
        self.oneval = inval

#newClass inherits functionality from myClass
class newClass (myClass):
    name = "Grant"
    #function to print class objects
    def __repr__(self):
        return self.name + ": oneval = " + str(self.oneval)


C = myClass(4)
B = myClass(10)
print(C.oneval)
print(C.div(32))
print(B.div(32))

N = newClass(12)
print(N.name)
print(N.div(36))
print(N)


#####
# try/except stuff
#####
try:
    print(N.div("ello"))
except TypeError:
    print("cant do that buster")


