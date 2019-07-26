from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *

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
    N=int(config[1])
    
    # Read privKey.txt
    with open("privKey.txt", "rb") as myFile:
        privKey = pickle.load(myFile)

    # Initialise CQC connection
    Alice=CQCConnection("Alice")

    # Signs message
    message=random.randint(0,pow(2,N)-1)
    print("Message is %d \n" % message)
    ACKSend(Alice, "Bob", [message]+privKey[message])

    # Close CQC connection
    Alice.close()

main()
