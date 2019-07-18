from random import randint, random, sample
from cqc.pythonLib import *
from time import sleep
from math import pi, sqrt, acos

# round((256/pi)*acos(sqrt(0.9)))

m = 3
n = 2
step = 14
estep = 256 - step
Bob_qubits = [ [] for i in range(n) ]
Alice_recv_qubits = [ [] for i in range(n) ]
wait = 0.5
def prep_Alice():

    with CQCConnection("Alice") as Alice:
    
        a_bits = [randint(0,1) for j in range(m)]
        c_bits = [[randint(0,1) for j in range(m)] for i in range(n)]
        print ("Step 1 is OK! in Alice Part")
        print ("a_bits:", a_bits)
        print ("c_bits:", c_bits)
        print ("Step 2 is starting")
        for i in range(n):
            for j in range(m):
                q_1 = qubit(Alice)
                q_2 = qubit(Alice)
                if (c_bits[i][j] == 0):
                  #  q_2.H()
                    q_1.rot_X(step)
                    q_2.rot_X(estep)
                else:
                  #  q_1.H()
                    q_1.rot_X(estep)
                    q_2.rot_X(step)

                Alice.sendQubit(q_1, "Bob")
                Alice.sendQubit(q_2, "Bob")
               
                bob_q1 = Alice.recvQubit()
                bob_q2 = Alice.recvQubit()
               
                Bob_qubits[i].append( (bob_q1,bob_q2) )
        Alice.flush()        
        # print ("Accepted Qubits by Alice from Bob:", Bob_qubits)
        print ("Step 3 is starting")
        for i in range(n):
            for j in range(m):
                
                e_ij = a_bits[j] ^ c_bits[i][j]
                print ("e_ij", e_ij)
                sleep(wait)
                Alice.sendClassical("Bob", e_ij)
                # sleep(wait)
                print("Alice is trying to accept f_ij:")
                sleep(wait)
                f_ij = Alice.recvClassical()[0]
                print("Accepted f_ij By Alice:", f_ij)
                alice_qubit = Alice.recvQubit()
                print("Alice receive qubit:", alice_qubit)
                Alice_recv_qubits[i].append(alice_qubit)
                
                print("The code can work until the if condition")
                if f_ij == 0:
                    Alice.sendQubit(Bob_qubits[i][j][1], "Bob")
                    Bob_qubits[i][j] = Bob_qubits[i][j][0]
                else:
                    Alice.sendQubit(Bob_qubits[i][j][0], "Bob")
                    Bob_qubits[i][j] = Bob_qubits[i][j][1]
        # print ("Alice_recv_qubits: ", Alice_recv_qubits)
        print ("Step 4 is starting")            
        # print("Receiving Qubits by Alice from Bob 2: ",Alice_recv_qubits )           
                # Or you can send this instead of the if block Alice.sendQubit(Bob_qubits[i][j][~f_ij])
        
        b_tilde = []
        for j in range(m):
            sleep(wait)
            Alice.sendClassical("Bob", a_bits[j])
            print ("Alice sent classical message: ", a_bits[j])
            sleep(wait)
            b_j = Alice.recvClassical()[0]
            print ("Alice receive classical message: ", b_j)
            for i in range(n):
                if b_j == 0:
                    Bob_qubits[i][j].rot_X(estep)
                    res = Bob_qubits[i][j].measure()
                    print ("res1", res)
                else:
                    Bob_qubits[i][j].rot_X(step)
                    res = Bob_qubits[i][j].measure()
                    print ("res2", res)
                if res != 0:
                    print("Cheating!")
                    break
            
            b_tilde.append(b_j)
            
            a_j_bar = 1 - a_bits[j]
           # print ("Step 5 is starting")
            for i in range(n):
                if a_j_bar == 0:
                    Alice_recv_qubits[i][j].rot_X(estep)
                    res = Alice_recv_qubits[i][j].measure()
                    print ("res1", res)
                else:
                    Alice_recv_qubits[i][j].rot_X(step)
                    res = Alice_recv_qubits[i][j].measure()
                    print ("res2", res)
                    
                if res != 0:
                    print("Cheating!")
                    break
        
        for i in range(m):
            if i==0:
                A = a_bits[i]
            else:
                A = A ^ a_bits[i]
        
        for i in range(m):
            if i==0:
                B_tilde = b_tilde[i]
            else:
                B_tilde = B_tilde ^ b_tilde[i]

        return A, B_tilde
        
if __name__ == "__main__":
    A, B_tilde = prep_Alice()
    x = A ^ B_tilde
    print("Shared coin toss is ", x)


                
