import sys
from random import randint, random, sample
from cqc.pythonLib import CQCConnection, qubit
from multiprocessing import Pool
from time import sleep


deltat = 5
receivedbasisbybob = []
basis_bob = []
receivebits = []
trueindex = []
truebits = []
def prep_Bob():

    with CQCConnection("Bob") as Bob:
        print("Starting")
        for i in range(10):
            q = Bob.recvQubit()
            random_basis_bob = randint(0,1)
            basis_bob.append(random_basis_bob)
            if random_basis_bob == 1:
               q.H()
            m = q.measure()
            receivebits.append(m)
        print("received bits: ", receivebits)    
        print("Basis produced by Bob: ",basis_bob)
        print("Now Alice and Bob are waiting on time:")
        sleep(deltat)    
        r = Bob.recvClassical()
        receivedbasisbybob[:] = list(r)
        print("Received basis by Bob: ", receivedbasisbybob)
        
        for i in range(len(receivebits)):
            if(receivedbasisbybob[i] == basis_bob[i]):
                print(i)
                trueindex.append(i)
                truebits.append(basis_bob[i])
        print("The final index: ", trueindex)
        print("The final bits: ",truebits)

if __name__ == "__main__":

    prep_Bob()
