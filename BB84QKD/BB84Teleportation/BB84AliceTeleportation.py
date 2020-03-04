import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from multiprocessing import pool
from cqc.pythonLib import CQCConnection, qubit
from teleportation import send_teleportation
from time import sleep


bits_alice = []
basis_alice = []
test = []
mesaj = []
wait = 1


def preperation_Alice():
    with CQCConnection("Alice") as location:
        for i in range(10):
            random_bits_alice = randint(0,1)
            random_basis_alice = randint(0,1)
            bits_alice.append(random_bits_alice)
            basis_alice.append(random_basis_alice)
            
            q = qubit(location)
            if random_bits_alice == 1:
                q.X()
         
            if random_basis_alice == 1:    
               q.H()
            #Alice.sendQubit(q, "Bob")
            send_teleportation(q,location,'Bob')
            test.append(random_bits_alice)
        location.flush()
        print ("Step 1 ok")
        sleep(wait)
        location.sendClassical("Bob", basis_alice)
        print ("Step 2 ok")
        print ("bits of alice:", bits_alice)
        print("sended basis by alice",basis_alice)

if __name__ == "__main__":

    preperation_Alice()

