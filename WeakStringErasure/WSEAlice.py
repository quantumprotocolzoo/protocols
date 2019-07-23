import sys
from random import randint, random, sample
from cqc.pythonLib import CQCConnection, qubit
from multiprocessing import Pool
from time import sleep

deltat = 5
bits_alice = []
basis_alice = []


def prep_Alice():

    with CQCConnection("Alice") as Alice:
        print("Starting")
        for i in range(10):
            random_bits_alice = randint(0,1)
            random_basis_alice = randint(0,1)
            bits_alice.append(random_bits_alice)
            basis_alice.append(random_basis_alice)
            q = qubit(Alice)
            if random_bits_alice == 1:
                q.X()
            if random_basis_alice == 1:    
                q.H()
            Alice.sendQubit(q, "Bob")
        print("Qubits were sent")
        Alice.flush()
        
       
        print("Now Alice and Bob are waiting on time:")
        sleep(deltat)
        # Alice.sendClassical("Bob", bits_alice)
        print("Alice sends her basis as classical messages: ", basis_alice)
        Alice.sendClassical("Bob", basis_alice)
        
if __name__ == "__main__":

    prep_Alice()
        
