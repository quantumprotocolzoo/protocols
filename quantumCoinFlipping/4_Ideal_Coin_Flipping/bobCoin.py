from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *

import random
import numpy
#########################################
#
# FUNCTIONS
#
def ACKSend(name, target, data):
    name.sendClassical(target, data)
    while bytes(name.recvClassical(msg_size=3)) != b'ACK':
        pass
    return 1

def ACKRecv(name, target):
    data = list(name.recvClassical())
    name.sendClassical(target, list(b'ACK'))
    return data

def measureInBasis(q, beta, y):
    q.rot_Z(128*beta)
    q.rot_Y(256-round((256/math.pi)*math.acos(math.sqrt(y))))
    m=q.measure()
    return m

def coinFlipBob(name, target, beta, y):
    q=name.recvQubit()
    m=measureInBasis(q, beta, y)
    measurement=[beta,m]
    ACKSend(name, target, list(b'ACK'))
    return measurement

#########################################
#
# MAIN
#
def main():
    # Get parameters
    y=0.9
    
    # Create string: beta_i in {0,1}
    beta=random.randint(0,1)

    # Initialise connection
    Bob=CQCConnection("Bob")

    # Bob performs the quantum part of the protocol until he makes a successful measurement
    measurement=coinFlipBob(Bob, "Alice", beta, y)
    
    # Bob calculates the position of his first successful measurement
    b=random.randint(0,1)

    # Bob sends the random bit, b, and j
    print("Bob sends b={}".format(b))
    ACKSend(Bob, "Alice", [b])

    # Bob receives c_j and alpha_j
    data=list(ACKRecv(Bob, "Alice"))
    alpha=data[0]
    c=data[1]

    # Bob computes the outcome of the coin flip
    if beta == alpha and measurement[1]==c:
        COIN=(b+c) % 2
    elif beta != alpha:
        COIN=(b+c) % 2
        print("Basis different")
    else:
        COIN=9
        print("ABORT")

    if COIN!=9:
        if COIN:
            winner="Bob"
        else:
            winner="Alice"
        
        to_print="{} WINS".format(winner)
        print("|"+"-"*(len(to_print)+2)+"|")
        print("| "+to_print+" |")
        print("|"+"-"*(len(to_print)+2)+"|")

    # Closes CQC connection
    Bob.close()

main()
