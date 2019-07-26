from random import randint, random, sample
from time import sleep
from cqc.pythonLib import CQCConnection, qubit



wait = 2
N = 10
M = 2
Alice_bits = [ [] for i in range(M) ]
Alice_basis = [[] for j in range(M)]
def preperation_and_controlling():
    print("The first part is starting and The bank prepare the moneys")
    with CQCConnection("Alice") as Alice:
        for serial in range(M): 
            for j in range(N):
                random_bits = randint(0,1)
                random_basis = randint(0,1)
                Alice_bits[serial].append(random_bits)
                Alice_basis[serial].append(random_basis)
                q = qubit(Alice)
                
                if random_bits == 1:
                    q.X()
             
                if random_basis == 1:    
                   q.H()
                Alice.sendQubit(q, "Bob")
                
        Alice.flush()
        print("Alice_bits ", Alice_bits)
        print("Alice_basis ", Alice_basis)
        print("Second part is starting: ")
        sleep(wait)
        serial = Alice.recvClassical()[0]
        print("Alice received classical message: ",serial)
        sleep(wait)
        for j in range(N):
            q = Alice.recvQubit()
            if Alice_basis[serial][j] == 1:
                q.H()
            m = q.measure()
            if m != Alice_bits[serial][j]:
                print("cheating! for this bit: ", m)
            print("The money is secure:", m)  
            
            
if __name__ == "__main__":      
    preperation_and_controlling()     
        
