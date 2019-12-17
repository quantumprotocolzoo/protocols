import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from multiprocessing import Pool
from cqc.pythonLib import CQCConnection, qubit


def B_party(num_bits, conn):

    basis_bob = [] 
    res_measure = []

    def preparation_Bob():
        q_arr = []
        for i in range(num_bits):
            q = conn.recvQubit()
            q_arr.append(q)
            
            
        for i in range(num_bits): 
            random_basis_bob = randint(0,1)
            basis_bob.append(random_basis_bob)
            if random_basis_bob == 1:
                q_arr[i].H()
            m = q_arr[i].measure()
            res_measure.append(m)

        print ("basis Bob:  ", basis_bob)
        print ("measurement results of Bob: ",res_measure)         


    def send_basis_toA():
        conn.sendClassical("Alice", basis_bob)

    def rec_keygen():
        matchList = conn.recvClassical()
        key_B=[]
        for i in matchList:
            key_B.append(res_measure[i])
        key_B = ''.join(map(str, key_B))
        print("key_B=",key_B)     
        return key_B
            
    preparation_Bob()
    send_basis_toA()
    return rec_keygen()
