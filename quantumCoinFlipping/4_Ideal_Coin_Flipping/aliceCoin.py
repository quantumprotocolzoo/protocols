from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *

import random
import numpy
import math
#########################################
#
# FUNCTIONS
#
def ACKSend(name, target, data):
    name.sendClassical(target, data)
    while bytes(name.recvClassical(msg_size=3)) != b'ACK':
        pass

def ACKRecv(name, target):
    data = list(name.recvClassical())
    name.sendClassical(target, list(b'ACK'))
    return data

def prepareQubit(name, alpha, c, y):
    q=qubit(name)
    if c==0:
        q.rot_Y(round((256/math.pi)*math.acos(math.sqrt(y))))
        q.rot_Z(128*alpha)
    elif c==1:
        q.rot_Y(round((256/math.pi)*math.acos(math.sqrt(1-y))))
        q.rot_Z(128*((alpha+1)%2))
    return q

def QcoinFlipAlice(name, target, aliceString,y):
    q=prepareQubit(name, aliceString[0], aliceString[1], y)
    name.sendQubit(q, target)
    ACKRecv(name, target)

#########################################
#
# MAIN
#
def main():
    # Get parameters
    y=0.9
    
    # Choose two bits: alpha in {0,1} and c in {0,1}
    aliceString=[random.randint(0,1),random.randint(0,1)]

    # Initialise connection
    Alice=CQCConnection("Alice")
        
    # Alice performs the quantum part of the protocol until Bob makes a successful measurement
    QcoinFlipAlice(Alice, "Bob", aliceString, y)
        
    # Alice receives the random bit and the position of first successful measurement from Bob
    data=list(ACKRecv(Alice, "Bob"))
    b=data[0]

    # Alice sends c and alpha
    print("Alice sends alpha={} and c={}".format(aliceString[0],aliceString[1]))
    ACKSend(Alice, "Bob", aliceString)

    # Alice computes the outcome of the coin flip
    COIN=(b+aliceString[1]) % 2

    # Closes CQC connection
    Alice.close()

main()
