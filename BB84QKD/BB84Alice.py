import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from multiprocessing import pool
from cqc.pythonLib import CQCConnection, qubit



bits_alice = []
basis_alice = []
test = []
mesaj = []



def preperation_Alice():
    with CQCConnection("Alice") as Alice:
        for i in range(100):
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
            
            '''
            if (random_basis_alice == 0 ):
                basis_alice.append('X')
            elif (random_basis_alice == 1):
                basis_alice.append('Z')
                '''
            test.append(random_bits_alice)
        Alice.flush()
        Alice.sendClassical("Bob", basis_alice)
        print ("bits of alice:", bits_alice)
        print("sended basis by alice",basis_alice)

if __name__ == "__main__":

    preperation_Alice()
