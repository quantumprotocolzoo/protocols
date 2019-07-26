#from SimulaQron.general.hostConfig import *
#from SimulaQron.cqc.backend.cqcHeader import *
#from SimulaQron.cqc.pythonLib.cqc import *
from cqc.pythonLib import CQCConnection, qubit

import random
import numpy
import pickle
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

###################################
#
# Main
#
def main():
    
    # Get parameters
    config=numpy.loadtxt("config.txt")
    
    # Reads signed message
    sgndMessage=list(numpy.loadtxt("bobSgndMessage.txt", dtype='int'))

    # Initialise CQC connection
    with CQCConnection("Bob") as Bob:
    
        # Forward message to Charlie
        ACKSend(Bob, "Charlie", sgndMessage)

main()
