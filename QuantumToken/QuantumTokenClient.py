from random import randint, random, sample
from time import sleep
from cqc.pythonLib import CQCConnection, qubit



M = 8
N = 2
wait = 2 
basis = []
serialnumbers = []
accepted_basis = []
measurements = []
trueindex = []
truebits = []
Bob_recv = [ [] for i in range(8) ]
bank_bits_pairs = [[] for i in range(N)]
accepted_qubits = []
def usage_money():
    with CQCConnection("Eve") as Eve:
        print("Client part is starting: ")
        for serial in range(M):
            for j in range(N):
                q1 = Eve.recvQubit()
                q2 = Eve.recvQubit()
                # accepted_qubits[j].append((q1,q2))
                # Eve.sendQubit(accepted_qubits[j],"Bob")
                Eve.sendQubit(q1, "Bob")    
                Eve.sendQubit(q2, "Bob")       
  
        print("The client(Eve) gave money to Merchant(Bob)")
        print ("Second stage is starting: ")   
      
        
        
if __name__ == "__main__":
    usage_money()
