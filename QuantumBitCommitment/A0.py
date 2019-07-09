import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from cqc.pythonLib import CQCConnection, qubit
from time import sleep

aclassic = []
aclassbasis = []
wait = 1

'''
In prep_Alice funtion:
produced n bit and saved in aclassic list
produced n basis and saved in aclassbasis list
produced n fresh qubits and according to produced bit and basis, (conditionally) applied gates and sent to B0
aclassic list was sent to A1 and A2
aclassbasis list was sent to A1 and A2
'''


def prep_Alice():

    with CQCConnection("A0") as A0:
        
         for i in range(10):
             random_bits_alice = randint(0,1)
             random_basis_alice = randint(0,1)
             aclassic.append(random_bits_alice)
             aclassbasis.append(random_basis_alice)
             q = qubit(A0)
           
             if random_bits_alice == 1:
                 q.X()
             if random_basis_alice == 1:    
                 q.H()
             A0.sendQubit(q, "B0")
         # , close_after=False
         A0.flush()
         sleep(wait)
         A0.sendClassical("A1",aclassic)
         print ("Aclassic was sent to A1")
         sleep(wait)
         A0.sendClassical("A1",aclassbasis)
         print ("AclassicBASIS was sent to A1")
         sleep(wait)
         A0.sendClassical("A2",aclassic)
         print ("Aclassic was sent to A2")
         sleep(wait)
         A0.sendClassical("A2",aclassbasis)
         print ("AclassicBASIS was sent to A2")
        # print ("HELLO")
         
         
if __name__ == "__main__":
    prep_Alice()

