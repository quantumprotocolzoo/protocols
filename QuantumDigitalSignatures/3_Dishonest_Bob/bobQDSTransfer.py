from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *

import random
import numpy
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
    L=int(config[0])
    
    # Get Bob's USE string
    bobStrings={0:numpy.loadtxt("B0.txt", dtype='int'),1:numpy.loadtxt("B1.txt", dtype='int')}

    # Load the symmetrised measurements from the files
    sgndMessage=list(numpy.loadtxt("bobSgndMessage.txt", dtype='int'))
    
    # Guess private key for forged message from USE String
    frgdMessage=(sgndMessage[0]+1) % 2
    frgdSignature=[1 if bobStrings[frgdMessage][x]==0 else 0 if bobStrings[frgdMessage][x]==1 else 2 if bobStrings[frgdMessage][x]==3 else 3 if bobStrings[frgdMessage][x]==2 else random.randint(0,3) for x in range (0,L)]
    
    # Initialise CQC connection
    Bob=CQCConnection("Bob")
    
    # Forge a message to send to Charlie
    forgedMessage=[frgdMessage]+frgdSignature
                     
    print("(dishonest)Bob forges message %d \n" % forgedMessage[0])
                     
    ACKSend(Bob, "Charlie", forgedMessage)

    # Close CQC connection
    Bob.close()

main()
