from cqc.pythonLib import CQCConnection, qubit

import math
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

def coinFlipBob(name, target, beta, y, K, transmission):
    measurements={0:[],1:[]}
    q=name.recvQubit()
    m=measureInBasis(q, beta[0], y)
    measurements[beta[0]].append(m)
    measurements[(beta[0]+1)%2].append('-')
    ACKSend(name, target, list(b'ACK'))
    for k in range (1,K):
        q=name.recvQubit()
        if random.random()>transmission:
            q.measure()
            measurements[0].append('-')
            measurements[1].append('-')
        else:
            m=measureInBasis(q, beta[k], y)
            measurements[beta[k]].append(m)
            measurements[(beta[k]+1)%2].append('-')
        ACKSend(name, target, list(b'ACK'))
    return measurements

def J(measurements, K):
    m00=K+1
    m01=K+1
    m10=K+1
    m11=K+1
    if measurements[0].count(0)>0:
        m00=measurements[0].index(0)
    if measurements[0].count(1)>0:
        m01=measurements[0].index(1)
    if measurements[1].count(0)>0:
        m10=measurements[1].index(0)
    if measurements[1].count(1)>0:
        m11=measurements[1].index(1)
    if min(m00,m01,m10,m11)==K+1:
        print("No Measurements made: ABORT")
    else:
        return min(m00,m01,m10,m11)
#########################################
#
# MAIN
#
def prep_bob():
    # Get parameters
    config=numpy.loadtxt("config.txt")
    K=int(config[0])
    y=float(config[1])
    transmission=float(config[2])
    
    # Create string: beta_i in {0,1}
    beta=[]
    for k in range (0,K):
        beta.append(random.randint(0,1))
    b=random.randint(0,1)

    # Initialise connection
    with CQCConnection("Bob") as Bob:

        # Bob performs the quantum part of the protocol until he makes a successful measurement
        measurements=coinFlipBob(Bob, "Alice", beta, y, K, transmission)

        # Bob calculates the position of his first successful measurement
        j=J(measurements, K)
        b=random.randint(0,1)

        # Bob sends the random bit, b, and j
        print("Bob sends b={} and j={}".format(b,j))
        ACKSend(Bob, "Alice", [b,j])

        # Bob receives c_j and alpha_j
        data=list(ACKRecv(Bob, "Alice"))
        alpha_j=data[0]
        c_j=data[1]

        # Bob computes the outcome of the coin flip
        if beta[j] ==alpha_j and measurements[beta[j]][j]==c_j:
            COIN=(b+c_j) % 2
        elif beta[j] != alpha_j:
            COIN=(b+c_j) % 2
            print("Basis different")
        else:
            COIN=9
            print("BOB detects cheating: ABORT")

        if COIN!=9:
            if COIN:
                winner="Bob"
            else:
                winner="Alice"

            to_print="{} WINS".format(winner)
            print("|"+"-"*(len(to_print)+2)+"|")
            print("| "+to_print+" |")
            print("|"+"-"*(len(to_print)+2)+"|")

if __name__ == "__main__" :
    prep_bob()
