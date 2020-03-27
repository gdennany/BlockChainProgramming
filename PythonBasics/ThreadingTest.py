import threading
import time
import random

def printA():
    for i in range(6):
        print("A "+ str(i) + " .... . ....")
        time.sleep(random.randint(1,4) * .1)
    return 89
def printB():
    for i in range(6):
        print("B " + str(i) + "***** * ****")
        time.sleep(random.randint(1,4) * .1)
def printAny(inpList):
    for i in inpList:
        print(str(i))
        time.sleep(random.randint(1,4) * .1)


t1 = threading.Thread(target = printA)

t2 = threading.Thread(target = printAny, args = ((789, "Ello", [1,2,3]), ))

t1.start()
t2.start()

printB()

t1.join()
t2.join()
print("END")