from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *

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
    for k in range (0,int(pow(2,N))):
        r=ACKRecv(name, target)
        l=random.sample(range(0, L), int(L/2))
        for x in l:
            operator.setitem(Send[k],x,USE[k][x])
            operator.setitem(Keep[k],x,9)
        message=message+Send[k]
    m=ACKRecv(name, target)
    ACKSend(name, target, message)
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
    if os.path.isfile("charlieKeep0.txt"):
        os.remove("charlieKeep0.txt")
    if os.path.isfile("charlieKeep1.txt"):
        os.remove("charlieKeep1.txt")
    if os.path.isfile("charlieReceived0.txt"):
        os.remove("charlieReceived0.txt")
    if os.path.isfile("charlieReceived1.txt"):
        os.remove("charlieReceived1.txt")

    # Load the USEs from the files
    charlieUSE={0:numpy.loadtxt("C0.txt", dtype='int'),1:numpy.loadtxt("C1.txt", dtype='int')}
    
    # Initialise CQC connection
    Charlie=CQCConnection("Charlie")
    
    # Tell Bob to begin symmetrisation
    ACKSend(Charlie, "Bob", list(b'ACK'))
    
    # Performs symmetrisation with Charlie
    charlieKeep, charlieReceived=symmetrisation(Charlie, "Bob", N, L, charlieUSE)

    # Writes these to text files
    cKeep0=open("charlieKeep0.txt", "a+")
    cKeep1=open("charlieKeep1.txt", "a+")
    cReceived0=open("charlieReceived0.txt", "a+")
    cReceived1=open("charlieReceived1.txt", "a+")
    
    for l in range (0,L):
        cKeep0.write("%d " % charlieKeep[0][l])
        cKeep1.write("%d " % charlieKeep[1][l])
        cReceived0.write("%d " % charlieReceived[0][l])
        cReceived1.write("%d " % charlieReceived[1][l])

    cKeep0.close()
    cKeep1.close()
    cReceived0.close()
    cReceived1.close()

    print("Charlie: SYMMETRISATION COMPLETE")

    # Close CQC connection
    Charlie.close()

main()
