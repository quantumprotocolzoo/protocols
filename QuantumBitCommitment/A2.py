from cqc.pythonLib import CQCConnection, qubit
from time import sleep

aclassic = []
aclassbasis = []
received2 = []
received1 = []
wait = 1

'''
A2 is the last station of this protocol
First, A2 accepts the knowledge from A0
After waiting a specific time for second phase,
Second A2 accepts the knowledge from B2
Third A2 accepts the knowledge from A1 
And A2 compares the knowledge that he received A1 and B2
'''


def part_A2():

    with CQCConnection("A2") as A2:
     sleep(wait)
     aclassic[:] = list(A2.recvClassical())
     sleep(wait)
     aclassbasis[:] = list(A2.recvClassical())
     
     print ("aclassic for A2:", aclassic)
     print ("aclassicbasis for A2:", aclassbasis)
     
     sleep(5)
     
     sleep(wait)
     received2[:] = list(A2.recvClassical())
     print ("received1 for A2:", received2)
     sleep(wait)
     commitment = A2.recvClassical()[0]
     print ("commitment for A2:", commitment)
     
    
     sleep(wait)
     received1[:] = list(A2.recvClassical())
     if(received2 != received1):
         cheat = True 
         print("Something is wrong!")
     else:
         print("Something is really GOOD!")        

if __name__ == "__main__":       
    part_A2()     
