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
def prepareQubit(name, alpha, c, y):
    q=qubit(name)
    if c==0:
        q.rot_Y(round((256/math.pi)*math.acos(math.sqrt(y))))
        q.rot_Z(128*alpha)
    elif c==1:
        q.rot_Y(round((256/math.pi)*math.acos(math.sqrt(1-y))))
        q.rot_Z(128*((alpha+1)%2))
    return q

def testState(name, y):
    x=5000
    # Test alpha=0, c=0
    count00=0
    count00H=0
    for i in range (0,x):
        q=prepareQubit(name, 0, 0, y)
        if q.measure()==1:
            count00=count00+1
    for i in range (0,x):
        q=prepareQubit(name, 0, 0, y)
        q.H()
        if q.measure()==1:
            count00H=count00H+1
    expected00=1-y
    expected00H=math.pow((math.sqrt(y)-math.sqrt(1-y)),2)/2
    count00=count00/x
    count00H=count00H/x

    # Test alpha=0, c=1
    count01=0
    count01H=0
    for i in range (0,x):
        q=prepareQubit(name, 0, 1, y)
        if measureInBasis(q,0,y)==1:
            count01=count01+1
    for i in range (0,x):
        q=prepareQubit(name, 0, 1, y)
        q.H()
        if measureInBasis(q,0,y)==1:
            count01H=count01H+1
    expected01=y
    expected01H=math.pow((math.sqrt(y)+math.sqrt(1-y)),2)/2
    count01=count01/x
    count01H=count01H/x
    
    # Test alpha=1, c=0
    count10=0
    count10H=0
    for i in range (0,x):
        q=prepareQubit(name, 1, 0, y)
        if measureInBasis(q,0,y)==1:
            count10=count10+1
    for i in range (0,x):
        q=prepareQubit(name, 1, 0, y)
        q.H()
        if measureInBasis(q,0,y)==1:
            count10H=count10H+1
    expected10=1-y
    expected10H=math.pow((math.sqrt(y)+math.sqrt(1-y)),2)/2
    count10=count10/x
    count10H=count10H/x
    
    # Test alpha=1, c=1
    count11=0
    count11H=0
    for i in range (0,x):
        q=prepareQubit(name, 1, 1, y)
        if measureInBasis(q,0,y)==1:
            count11=count11+1
    for i in range (0,x):
        q=prepareQubit(name, 1, 1, y)
        q.H()
        if measureInBasis(q,0,y)==1:
            count11H=count11H+1
    expected11=y
    expected11H=math.pow((math.sqrt(1-y)-math.sqrt(y)),2)/2
    count11=count11/x
    count11H=count11H/x
    print("count00 = %.3f" % count00)
    print("expected00 = %.3f" % expected00)
    print("--------------------------------")
    print("count00H = %.3f" % count00H)
    print("expected00H = %.3f" % expected00H)
    print("--------------------------------")
    print("count00 = %.3f" % count01)
    print("expected00 = %.3f" % expected01)
    print("--------------------------------")
    print("count00H = %.3f" % count01H)
    print("expected00H = %.3f" % expected01H)
    print("--------------------------------")
    print("count00 = %.3f" % count10)
    print("expected00 = %.3f" % expected10)
    print("--------------------------------")
    print("count00H = %.3f" % count10H)
    print("expected00H = %.3f" % expected10H)
    print("--------------------------------")
    print("count00 = %.3f" % count11)
    print("expected00 = %.3f" % expected11)
    print("--------------------------------")
    print("count00H = %.3f" % count11H)
    print("expected00H = %.3f" % expected11H)
    print("--------------------------------")

def measureInBasis(q, beta, y):
    q.rot_Z(128*beta)
    q.rot_Y(256-round((256/math.pi)*math.acos(math.sqrt(y))))
    m=q.measure()
    return m

#########################################
#
# MAIN
#
def main():
    # Get parameters
    config=numpy.loadtxt("config.txt")
    K=int(config[0])
    y=float(config[1])

    # Initialise connection
    Alice=CQCConnection("Alice")

    # Alice performs the test
    testState(Alice, y)

    # Closes CQC connection
    Alice.close()

main()
