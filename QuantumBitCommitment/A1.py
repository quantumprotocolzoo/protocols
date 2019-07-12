from cqc.pythonLib import CQCConnection, qubit
from time import sleep
aclassic = []
aclassbasis = []
received1 = []
wait = 1

'''
A1, first accepts knowledges(aclassic and aclassbasis) from A0 
After waiting a specific time for second phase this time A1 accepts
the knowledges from B1 and it does some tests 
after these tests A1 sends knowledge to A2. 
'''


def part_A1():

    with CQCConnection("A1") as A1:
        sleep(wait)
        aclassic[:] = list(A1.recvClassical())
        print ("aclassic for A1:", aclassic)
        sleep(wait)
        aclassbasis[:] = list(A1.recvClassical())
        print ("aclassicbasis for A1:", aclassbasis)
        sleep(5)
        
        sleep(wait)
        c = A1.recvClassical()
        received1[:] = list(c)
        print ("received1 was transformed for A1:", received1)
        sleep(wait)
        commitment = A1.recvClassical()[0]
        print ("commitment for A1:", commitment)
     
        cheat = False
        for i in range(len(aclassic)):
            if (commitment == aclassbasis[i]):
                if (aclassic[i] == received1[i]):
                    print("qubit", i, "is OK!")
                    continue
                else:
                    print("Bob is Cheating")
                    cheat = True    
                    break
        sleep(wait)
        A1.sendClassical("A2", received1)
     
     
if __name__ == "__main__":       
    part_A1()     
