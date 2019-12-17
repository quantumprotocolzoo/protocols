import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from multiprocessing import pool
from cqc.pythonLib import CQCConnection, qubit


def A_party(num_bits, conn):

    bits_alice = []
    basis_alice = []

    def preperation_Alice():
        for i in range(num_bits):
            random_bits_alice = randint(0,1)
            random_basis_alice = randint(0,1)
            bits_alice.append(random_bits_alice)
            basis_alice.append(random_basis_alice)

            q = qubit(conn)
        
            if random_bits_alice == 1:
                q.X()
        
            if random_basis_alice == 1:    
                q.H()
            conn.sendQubit(q, "Bob")
        print("bits Alice:",bits_alice)
        print("basis Alice:",basis_alice)

    def compare_basis(basis_alice,basis_bob):
        matchList=[]
        for i in range(len(basis_alice)):
            if basis_alice[i] == basis_bob[i]: #measure in standard basis
                matchList.append(i)
            else:
                pass
        return matchList

    def rec_com_send():
        basis_bob = conn.recvClassical()
        #print(basis_bob)
        matchList=compare_basis(basis_alice,basis_bob)
        print("matchList=",matchList)
        conn.sendClassical("Bob", matchList)
        return matchList

    def keygen(matchList):
        key_A=[]
        for i in matchList:
            key_A.append(bits_alice[i]) #quantum state 0,+:0    1,-:1
        
        key_A = ''.join(map(str, key_A))
        return key_A

    preperation_Alice()
    return keygen(rec_com_send())


