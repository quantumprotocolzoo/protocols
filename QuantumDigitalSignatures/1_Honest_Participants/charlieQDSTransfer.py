#from SimulaQron.general.hostConfig import *
#from SimulaQron.cqc.backend.cqcHeader import *
#from SimulaQron.cqc.pythonLib.cqc import *
from cqc.pythonLib import CQCConnection, qubit

import random
import numpy
import pickle
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

def verify(name, L, dictionary, sv):
    Keep=dictionary['Keep']
    Received=dictionary['Received']
    sgndMessage=dictionary['sgndMessage']
    countKeep=0
    countReceived=0
    message=sgndMessage[0]
    signature=sgndMessage[1:L+2]
    for l in range (0,L):
        if signature[l]==Keep[message][l]:
            countKeep=countKeep+1
        if signature[l]==Received[message][l]:
            countReceived=countReceived+1
    if float(countKeep)<=float(sv*L/2) and float(countReceived)<=float(sv*L/2):
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
    sv=float(config[3])
    
    # Load the symmetrised measurements from the files
    dictionary={'Keep':{0:numpy.loadtxt("charlieKeep0.txt", dtype='int'),1:numpy.loadtxt("charlieKeep1.txt", dtype='int')},'Received':{0:numpy.loadtxt("charlieReceived0.txt", dtype='int'),1:numpy.loadtxt("charlieReceived1.txt", dtype='int')}}
    
    # Initialise CQC connection
    with CQCConnection("Charlie") as Charlie:

        # Receive message from Bob
        dictionary['sgndMessage']=ACKRecv(Charlie, "Bob")

        # Verify message using the two measurement strings Keep and Received
        v, countKeep, countReceived=verify(Charlie, L, dictionary, sv)
        if v:
            print("CHARLIE ACCEPTS")
        else:
            print("CHARLIE ABORTS")

        print("Charlie counted {} direct mismatches and {} received mismatches".format(countKeep, countReceived))
        print("Charlie's threshold is {}".format(sv*L/2))

        # Saves the signed message to txt file
        if os.path.isfile("charlieSgndMessage.txt"):
            os.remove("charlieSgndMessage.txt")
        charlie=open("charlieSgndMessage.txt", "a+")
        for l in range (0,L):
            charlie.write("%d " % dictionary['sgndMessage'][l])

main()
