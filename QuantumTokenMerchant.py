from random import randint, random, sample
from time import sleep
from cqc.pythonLib import CQCConnection, qubit


M = 8
N = 2
wait = 2 
results_of_qubit =  [ [] for i in range(M) ]
accepted_qubits_from_client = []

def merchants():
    with CQCConnection("Bob") as Bob:
    
        for serial in range(M): 
            for j in range(N):
                q1 = Bob.recvQubit()
                q2 = Bob.recvQubit()
                random_bit = randint(0,1)
                if random_bit == 1:
                    q1.H()
                    q2.H()
                m1 = q1.measure()
                m2 = q2.measure()
                results_of_qubit[j].append((m1, m2,random_bit))
        for serial in range(M): 
            for j in range(N):
                sleep(wait) 
                Bob.sendClassical("Alice", results_of_qubit[j][serial])    
                print("Now the merchant sent the outcomes and basis to the bank: ",results_of_qubit[j][serial] )
                sleep(wait)
        print("Now the merchant sent all")     
                    
                
if __name__ == "__main__":
    merchants()
