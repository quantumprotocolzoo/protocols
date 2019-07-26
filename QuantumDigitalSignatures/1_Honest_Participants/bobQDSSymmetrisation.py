#from SimulaQron.general.hostConfig import *
#from SimulaQron.cqc.backend.cqcHeader import *
#from SimulaQron.cqc.pythonLib.cqc import *
from cqc.pythonLib import CQCConnection, qubit

import random
import numpy
import os
import operator
###################################
#
# Functions
#
def ACKSend(name, target, data):
    name.sendClassical(target, data)
    while bytes(name.recvClassical(msg_size=3)) != b'ACK':
        pass
                
def ACKRecv(name, target):
    data = list(name.recvClassical())
    name.sendClassical(target, list(b'ACK'))
    return data

def symmetrisation(name, target, N, L, USE):
    Keep=USE
    Send={0:[9]*L,1:[9]*L}
    Received={}
    message=[]
    for k in range (0,pow(2,N)):
        ACKSend(name, target, 1)
        l=random.sample(range(0, L), int(L/2))
        for x in l:
            operator.setitem(Send[k],x,USE[k][x])
            operator.setitem(Keep[k],x,9)
        message=message+Send[k]
    ACKSend(name, target, message)
    m=ACKRecv(name, target)
    for k in range(0,pow(2,N)):
        Received[k]=m[k*L:(k+1)*L]
    return Keep, Received

###################################
#
# Main
#
def main():
    
    # Get parameters
    config=numpy.loadtxt("config.txt")
    L=int(config[0])
    N=int(config[1])
    
    # Check existence of keep and received files and delete if found.
    if os.path.isfile("bobKeep0.txt"):
        os.remove("bobKeep0.txt")
    if os.path.isfile("bobKeep1.txt"):
        os.remove("bobKeep1.txt")
    if os.path.isfile("bobReceived0.txt"):
        os.remove("bobReceived0.txt")
    if os.path.isfile("bobReceived1.txt"):
        os.remove("bobReceived1.txt")

    # Load the USEs from the files
    bobUSE={0:numpy.loadtxt("B0.txt", dtype='int'),1:numpy.loadtxt("B1.txt", dtype='int')}

    # Initialise CQC connection
    with CQCConnection("Bob") Bob: 

        # Wait for Charlie to be ready for symmetrisation
        while bytes(ACKRecv(Bob, "Charlie")) != b'ACK':
            pass

        # Performs symmetrisation with Charlie
        bobKeep, bobReceived=symmetrisation(Bob, "Charlie", N, L, bobUSE)

        # Writes these to text files
        bKeep0=open("bobKeep0.txt", "a+")
        bKeep1=open("bobKeep1.txt", "a+")
        bReceived0=open("bobReceived0.txt", "a+")
        bReceived1=open("bobReceived1.txt", "a+")

        for l in range (0,L):
            bKeep0.write("%d " % bobKeep[0][l])
            bKeep1.write("%d " % bobKeep[1][l])
            bReceived0.write("%d " % bobReceived[0][l])
            bReceived1.write("%d " % bobReceived[1][l])

        bKeep0.close()
        bKeep1.close()
        bReceived0.close()
        bReceived1.close()

        print("Bob: SYMMETRISATION COMPLETE")

main()
