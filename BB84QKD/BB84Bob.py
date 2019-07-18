import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from multiprocessing import Pool
from cqc.pythonLib import CQCConnection, qubit

correct_basis = []
correct_key = []
bits_alice = []
basis_alice = []
bits_bob = []
basis_bob = [] 
received = []

def preparation_Bob():
    with CQCConnection("Bob") as Bob:
        for i in range(100):
            
            q = Bob.recvQubit()
            random_basis_bob = randint(0,1)
            basis_bob.append(random_basis_bob)
            if random_basis_bob == 1:
               q.H()
            m = q.measure()
            received.append(m)
            
        r = Bob.recvClassical()
        basis_alice[:] = list(r)
        
    print ("basis of bob ", basis_bob)
    print ("measurement results of bob: ",received)
    print ("received basis by bob ",basis_alice)
    
def calculate(): 
    error = 0
    for i in range(len(received)):
        if (basis_alice[i] == basis_bob[i]):
            correct_basis.append(i)
            correct_key.append(received[i])
        else:
            error = error + 1  
    print ("Correct Basis: ", correct_basis)        
    print ("Correct Key :", correct_key)
    print ("error:", error)
    error_percentage = error/len(received) # maximum value is 1
    print("error_percentage", error_percentage)
    size = ceil(sqrt(len(correct_basis)))
    print ("size: ", size) 
    global qber
    global qber2
    qber = error_percentage/size # lies btween 0 and 1
    print("qber:", qber)

def secureKeyRate(x):
    return ((-x)*log(x, 2) - (1-x)*log(1-x, 2))


if __name__ == "__main__":

    preparation_Bob()
    calculate()

