import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from multiprocessing import pool
from cqc.pythonLib import CQCConnection, qubit


correct_basis = []
bits_alice = []

basis_alice = []
bits_bob = []
basis_bob = [] 
received = []
test = []
mesaj = []



def preperation_Alice():
    with CQCConnection("Alice") as Alice:
        for i in range(100):
            random_bits_alice = randint(0,1)
            random_basis_alice = randint(0,1)
            bits_alice.append(random_bits_alice)
            basis_alice.append(random_basis_alice)
           # random_basis_alice = randint(0,1)
            q = qubit(Alice)
           
            if random_bits_alice == 1:
                q.X()
                #Alice.sendQubit(q, "Bob")
                # message = (0 + random_bits_alice) % 2
                # Alice.sendClassical("Bob", message)
                # mesaj.append(message)
         
            if random_basis_alice == 1:    
               q.H()
            Alice.sendQubit(q, "Bob")
            
           # random_bits_alice = (0 + random_bits_alice) % 2
           # bits_alice.append(random_bits_alice)
           # test.append(random_basis_alice)
           # Alice.sendClassical("Bob", random_bits_alice)
            '''
            if (random_basis_alice == 0 ):
                basis_alice.append('X')
            elif (random_basis_alice == 1):
                basis_alice.append('Z')
                '''
            #print("sended basis by alice",random_bits_alice)
            test.append(random_bits_alice)
        Alice.flush()
       # for i in basis_alice:
        Alice.sendClassical("Bob", basis_alice)
       # Alice.sendClassical("Bob", basis_alice)
        print ("bits of alice:", bits_alice)
        print("sended basis by alice",basis_alice)
     #   print ("message", mesaj)
    #    print ("basis of alice:", basis_alice)
     #   print("sended qubit by alice", m)


if __name__ == "__main__":

    preperation_Alice()
