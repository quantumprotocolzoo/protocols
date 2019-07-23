#from SimulaQron.general.hostConfig import *
#from SimulaQron.cqc.backend.cqcHeader import *
#from SimulaQron.cqc.pythonLib.cqc import *
from cqc.pythonLib import CQCConnection, qubit

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

def addNoise(q, noise):
    if random.random()<noise:
        q.X()
    if random.random()<noise:
        q.Z()
    return q

def prepareQubit(name, alpha, c, y, noise):
    q=qubit(name)
    if c==0:
        q.rot_Y(round((256/math.pi)*math.acos(math.sqrt(y))))
        q.rot_Z(128*alpha)
    elif c==1:
        q.rot_Y(round((256/math.pi)*math.acos(math.sqrt(1-y))))
        q.rot_Z(128*((alpha+1)%2))
    q=addNoise(q, noise)
    return q

def QcoinFlipAlice(name, target, aliceString, y, K, noise):
    for k in range (0,K):
        q=prepareQubit(name, aliceString['alpha'][k], aliceString['c'][k], y, noise)
        name.sendQubit(q, target)
        ACKRecv(name, target)

#########################################
#
# MAIN
#
def prep_alice():
    # Get parameters
    config=numpy.loadtxt("config.txt")
    K=int(config[0])
    y=float(config[1])
    noise=float(config[3])
    
    # Create strings: alpha_i in {0,1} and c_i in {0,1}
    aliceString={'alpha':[],'c':[]}
    for k in range (0,K):
        aliceString['alpha'].append(random.randint(0,1))
        aliceString['c'].append(random.randint(0,1))
    # Initialise connection
    with CQCConnection("Alice") as Alice:

        # Alice performs the quantum part of the protocol until Bob makes a successful measurement
        QcoinFlipAlice(Alice, "Bob", aliceString, y, K, noise)

        # Alice receives the random bit and the position of first successful measurement from Bob
        data=list(ACKRecv(Alice, "Bob"))
        b=data[0]
        j=data[1]
        # Alice sends c_j and alpha_j
        print("Alice sends alpha_j={} and c_j={}".format(aliceString['alpha'][j],aliceString['c'][j]))
        ACKSend(Alice, "Bob", [aliceString['alpha'][j],aliceString['c'][j]])

        # Alice computes the outcome of the coin flip
        COIN=(b+aliceString['c'][j]) % 2

if __name__ == "__main__":
    prep_alice()
