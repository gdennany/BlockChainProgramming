######
# Basic Data Types
######

#lists are mutable
mylist = [1,2,3,4]
mylist[2] = 5
print(mylist)

#dictionaries are mutable
mydict = {'A':1, 'B':2, 45:3}
print(mydict)
print(mydict['B'])
mydict['B'] = 6
print(mydict['B'])

#tuples are not mutable
tup = (54, "ello", [1,2,3,4])
#tup[1] = "hello" => error 
print(tup)
tup[2][1] = 5
print(tup)

print(type(tup))


######
# functions, loops, if statements
######

#fucntions
def myFunc(x):
    return "Anything"
    #note: python is weakly typed => can pass whatever and return whatever 
    #      without specifying what youre doing


#how to create main method:
if __name__ == '__main__':
    print(myFunc("something"))

#if, elif, else
if (False):
    print("in if")
elif (False):
    print("in elif")
else:
    print('in else')



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


C = myClass(4)
B = myClass(10)
print(C.oneval)
print(C.div(32))
print(B.div(32))