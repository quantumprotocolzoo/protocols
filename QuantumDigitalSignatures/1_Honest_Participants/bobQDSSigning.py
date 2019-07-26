#from SimulaQron.general.hostConfig import *
#from SimulaQron.cqc.backend.cqcHeader import *
#from SimulaQron.cqc.pythonLib.cqc import *
from cqc.pythonLib import CQCConnection, qubit

import random
import numpy
import os
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

def verify(name, L, dictionary, sa):
    Keep=dictionary['Keep']
    Received=dictionary['Received']
    sgndMessage=dictionary['sgndMessage']
    countKeep=0
    countReceived=0
    message=sgndMessage[0]
    signature=sgndMessage[1:L+1]
    for l in range (0,L):
        if signature[l]==Keep[message][l]:
            countKeep=countKeep+1
        if signature[l]==Received[message][l]:
            countReceived=countReceived+1
    if float(countKeep)<=float(sa*L/2) and float(countReceived)<=float(sa*L/2):
        return 1, countKeep, countReceived
    else:
        return 0, countKeep, countReceived

###################################
#
# Main
#
def main():
    
    # Get parameters
    config=numpy.loadtxt("config.txt")
    L=int(config[0])
    sa=float(config[2])
    
    # Load the symmetrised measurements from the files
    dictionary={'Keep':{0:numpy.loadtxt("bobKeep0.txt", dtype='int'),1:numpy.loadtxt("bobKeep1.txt", dtype='int')},'Received':{0:numpy.loadtxt("bobReceived0.txt", dtype='int'),1:numpy.loadtxt("bobReceived1.txt", dtype='int')}}

    # Initialise CQC connection
    with CQCConnection("Bob") as Bob:
    
        # Receive message from Alice
        dictionary['sgndMessage']=list(ACKRecv(Bob, "Alice"))

        # Verify message using the two measurement strings Keep and Received
        v, countKeep, countReceived = verify(Bob, L, dictionary, sa)
        if v:
            print("BOB ACCEPTS")
        else:
            print("BOB ABORTS")

        print("Bob counted {} direct mismatches and {} received mismatches".format(countKeep, countReceived))
        print("Bob's threshold is {}".format(sa*L/2))

        # Saves the signed message to txt file
        if os.path.isfile("bobSgndMessage.txt"):
            os.remove("bobSgndMessage.txt")
        bob=open("bobSgndMessage.txt", "a+")
        for l in range (0,L+1):
            bob.write("%d " % dictionary['sgndMessage'][l])

main()
