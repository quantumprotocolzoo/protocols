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

def distribute_quantum_signature(name, target, N, L, privKey, noise):
    ACKSend(name, target, list(b'ACK'))
    for k in range (0,pow(2,N)):
        for l in range(0,L):
            # Encoding is 0->|0>, 1->|1>, 2->|+>, 3->|->
            q=qubit(name)
            if privKey[k][l]==1:
                q.X()
            if privKey[k][l]==2:
                q.H()
            if privKey[k][l]==3:
                q.X()
                q.H()
            q=addNoise(q, noise)
            name.sendQubit(q, target)
            ACKRecv(name, target)
    return 1

def dishonest_distribute_quantum_signature(name, target, N, L, privKey, noise, e):
    ACKSend(name, target, list(b'ACK'))
    for k in range (0,pow(2,N)):
        for l in range(0,L):
            # Encoding is 0->|0>, 1->|1>, 2->|+>, 3->|->, Alice chooses a mismatch with probability e
            q=qubit(name)
            if privKey[k][l]==0 and random.random()<e:
                q.X()
            if privKey[k][l]==1 and random.random()>e:
                q.X()
            if privKey[k][l]==2:
                if random.random()<e:
                    q.X()
                q.H()
            if privKey[k][l]==3:
                if random.random()>e:
                    q.X()
                q.H()
            q=addNoise(q, noise)
            name.sendQubit(q, target)
            ACKRecv(name, target)
    return 1

def addNoise(q, noise):
    if random.random()<noise:
        q.X()
    if random.random()<noise:
        q.Z()
    return q


###################################
#
# Main
#
def main():
    # Get parameters
    config=numpy.loadtxt("config.txt")
    L=int(config[0])
    N=int(config[1])
    sa=float(config[2])
    sv=float(config[3])
    noise=float(config[4])
    e=(sa+sv)

    # Generate private key
    privKey={}
    for k in range (0,pow(2,N)):
        privKey[k]=[]
        for l in range (0,L):
            privKey[k].append(random.randint(0,3))
    with open("privKey.txt", "wb") as myFile:
        pickle.dump(privKey, myFile)

    # Initialise CQC connection
    Alice=CQCConnection("Alice")

    # Distribute the public (quantum) key
    distribute_quantum_signature(Alice, "Bob", N, L, privKey, noise)
    dishonest_distribute_quantum_signature(Alice, "Charlie", N, L, privKey, noise, e)

    # Confirm that distribution is complete
    ACKSend(Alice, "Bob", list(b'ACK'))
    ACKSend(Alice, "Charlie", list(b'ACK'))
    print("(dishonest)Alice: DISTRIBUTION COMPLETE")

    # Close CQC connection
    Alice.close()

main()
