from random import randint
from cqc.pythonLib import CQCConnection, qubit
from time import sleep
from math import pi, sqrt, acos

m = 3
n = 2
step = 14
estep = 256 - step
wait = 0.5
Alice_qubits = [ [] for i in range(n) ]
Bob_recv_qubits = [ [] for i in range(n) ]

def prep_Bob():

    with CQCConnection("Bob") as Bob:
        
        b_bits = [randint(0,1) for j in range(m)]
        d_bits = [[randint(0,1) for j in range(m)] for i in range(n)]

        print ("Step 1 is OK! in Bob Part ")
        print ("b_bits", b_bits)
        print ("d_bits", d_bits)

        print ("Step 2 is starting")
        for i in range(n):
            for j in range(m):
                q_1 = qubit(Bob)
                q_2 = qubit(Bob)

                if (d_bits[i][j] == 0):
                    q_1.rot_X(step)
                    q_2.rot_X(estep)
                else:
                    q_1.rot_X(estep)
                    q_2.rot_X(step)
                
                alice_q1 = Bob.recvQubit() 
                alice_q2 = Bob.recvQubit()
                    
                Bob.sendQubit(q_1, "Alice")
                Bob.sendQubit(q_2, "Alice")
                
                Alice_qubits[i].append( (alice_q1,alice_q2) )
        Bob.flush()        

        print("Step 3 is starting")
        for i in range(n):
            for j in range(m):
                f_ij = b_bits[j] ^ d_bits[i][j]
                print ("f_ij", f_ij)
                sleep(wait)
                e_ij = Bob.recvClassical()[0]
                print("Accepted e_ij By Bob:", e_ij)
                sleep(wait)
                Bob.sendClassical("Alice", f_ij)
                print("Bob sent the message:", f_ij)
                
                print("The code can work until the if condition")
                if e_ij == 0:
                    Bob.sendQubit(Alice_qubits[i][j][1], "Alice")
                    Alice_qubits[i][j] = Alice_qubits[i][j][0]
                else:
                    Bob.sendQubit(Alice_qubits[i][j][0], "Alice")
                    Alice_qubits[i][j] = Alice_qubits[i][j][1]   
                    
                bob_qubit = Bob.recvQubit()
                print("Bob receive qubit:", bob_qubit)
                Bob_recv_qubits[i].append(bob_qubit)
                 
        print("Step 4 is starting")              
        a_tilde = []
        for j in range(m):
            sleep(wait)
            a_j = Bob.recvClassical()[0]
            print("Bob receive message a_j: ", a_j)
            sleep(wait)
            Bob.sendClassical("Alice", b_bits[j])
            print ("Bob sent classical message:", b_bits[j])
            
            for i in range(n):
                if a_j == 0:
                    Alice_qubits[i][j].rot_X(estep)   
                    res = Alice_qubits[i][j].measure()
                    print("res1", res)
                else:
                    Alice_qubits[i][j].rot_X(step)    
                    res = Alice_qubits[i][j].measure()
                    print("res2", res)
                if res != 0:
                    print("Cheating!")
                    break

            a_tilde.append(a_j)
            
            b_j_bar = 1 - b_bits[j]
            for i in range(n):
                if b_j_bar == 0:
                    Bob_recv_qubits[i][j].rot_X(estep) 
                    res = Bob_recv_qubits[i][j].measure()
                    print ("res1", res)
                else:
                    Bob_recv_qubits[i][j].rot_X(step) 
                    res = Bob_recv_qubits[i][j].measure()
                    print ("res2", res)
                if res != 0:
                    print("Cheating!")
                    break
                    
        for i in range(m):
            if i==0:
                B = b_bits[i]
            else:
                B = B ^ b_bits[i]
        
        for i in range(m):
            if i==0:
                A_tilde = a_tilde[i]
            else:
                A_tilde = A_tilde ^ a_tilde[i]
         
        return B, A_tilde

if __name__ == "__main__":
    B, A_tilde = prep_Bob()
    x = B ^ A_tilde
    print("Shared coin toss is ", x)
                    
                    
                    
                    
