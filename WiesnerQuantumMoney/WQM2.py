from random import randint, random, sample
from time import sleep
from cqc.pythonLib import CQCConnection, qubit

M = 2
N = 10
wait = 2 
basis = []
serialnumbers = []
accepted_basis = []
measurements = []
trueindex = []
truebits = []
Bob_recv = [ [] for i in range(N) ]

def usage_money():
    with CQCConnection("Bob") as Bob:
        for serial in range(M):
            for j in range(N):
                q = Bob.recvQubit()
                Bob_recv[serial].append(q)
        sleep(wait)    
        print("Second part is starting")
        serial = randint(0,M-1)
        sleep(wait)   
        Bob.sendClassical("Alice", serial)
        print("serial has been sent: ", serial)
        sleep(wait)    
        for j in range(N):
            Bob.sendQubit(Bob_recv[serial][j], "Alice")
        print("qubits have been sent!")
        
if __name__ == "__main__":
    usage_money()
              
