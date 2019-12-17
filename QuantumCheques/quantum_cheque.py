from cqc.pythonLib import CQCConnection, qubit
from one_way_function import one_way_function
#from swap_test import swap_test
from threading import Thread
from random import *
import numpy as np
from swap_test import *
from A_party import A_party
from B_party import B_party

len_BB84_key = 8
db_id = 1
pk = 3
sk = 4
M = 400
cheque = []

n = 24


def measure(conn, q):
    # Measure qubit
    m=q.measure()
    to_print="App {}: Measurement outcome is: {}".format(conn.name,m)
    # print("|"+"-"*(len(to_print)+2)+"|")
    # print("| "+to_print+" |")
    # print("|"+"-"*(len(to_print)+2)+"|")
    return m

class ThreadAlice(Thread):

    def run(self):
        with CQCConnection("Alice") as Alice:

            # Alice uses her supplementary information like:
            # M: amount of money
            # db_id: database ID
            # r: random salting parameter
            # To form a unique key and generates a hashed quantum state
            # from that unique key using the quantum one way function
            print('===== BEGIN BB84 QKD Protocol ===== \n')
            print('[Alice]: Start BB84 Protocol')
            BB84_key = A_party(len_BB84_key, Alice)
            print('[Alice]: End BB84 Protocol')

            # Alice recieves two qubits of every GHZ state from Bank: A1 and A2
            qA_arr = []
            qforC_arr = []
            for i in range(0, n):
                qA = Alice.recvEPR()
                qA_arr.append(qA)
            print('[Alice]: Receives ' +str(n) + ' A qubit group of GHZ state from Bob' )

            for i in range(0, n):
                qforC = Alice.recvQubit()
                qforC_arr.append(qforC)
            print('[Alice]: Receives ' +str(n) + ' C qubit group of GHZ state from Bob \n' )
            print('===== END intial GHZ generation and distribution ===== \n \n')

            M = int(input("[Alice]: Enter amount of money you want to sign:"))

            print('\n \n ===== BEGIN Quantum One Way Function encoding and Bell state measurement ===== \n')
            print('[Alice]: Encodes a quantum one way function using db_id, random salt and amount of money')
            for i in range(0, n):
                r = randint(0, 1)
                owf_state = one_way_function(Alice, BB84_key, db_id, r, M)

                # Alice now performs Bell state measurement between
                # her state A1 and the state produced from the quantum one way function
                # To collapse the state and encode the information with the qubit A2
                owf_state.cnot(qA_arr[i])
                owf_state.H()

                qA_measure_result = measure(Alice, qA_arr[i])
                owf_state_measure_result = measure(Alice, owf_state)

                if qA_measure_result == 0 and owf_state_measure_result == 1:
                    qforC_arr[i].Z()
                if qA_measure_result == 1 and owf_state_measure_result == 0:
                    qforC_arr[i].X()
                if qA_measure_result == 1 and owf_state_measure_result == 1:
                    qforC_arr[i].Y()

                # Here the qubit A2 is ready as the cheque
                cheque_i = {'db_id': db_id, 'r': r, 'M': M}
                cheque.append(cheque_i)
            print('[Alice]: Performs Bell state measurement on state produced by quantum one way function and group A of GHZ state, to collapse the state and encode information to the group B and C of GHZ state')
            print('\n ===== END Quantum One Way Function encoding and Bell state measurement ===== \n \n')

            print('===== BEGIN SENDING CHEQUE TO CHARLIE ===== \n')
            # A2 qubit (cheque) is transferred to Charlie
            print('[Alice]: Sends ' +str(n) + ' C qubit group (The cheque) of GHZ states to Charlie' )
            for i in range(0, n):
                Alice.sendQubit(qforC_arr[i], "Charlie")
            

class ThreadCharlie(Thread):

    def run(self):
        with CQCConnection("Charlie") as Charlie:
            # Charlie receives the cheque from Alice
            qC_arr = []
            for i in range(0, n):
                qC = Charlie.recvQubit()
                qC_arr.append(qC)
            print('[Charlie]: Receives ' +str(n) + ' C qubit group (The cheque) of GHZ states from Alice\n')

            print('===== END cheque sending ===== \n \n')

            print('===== BEGIN Submitting cheque to Bank ===== \n')
            # Charlie sends the cheque to Bank (Bob) to cash it
            for i in range(0, n):
                Charlie.sendQubit(qC_arr[i], "Bob")
            print('[Charlie]: Sends ' +str(n) + ' C qubit group (The cheque) of GHZ states to Bank: To cash out \n' )
            
class ThreadBank(Thread):

    def run(self):
        with CQCConnection("Bob") as Bob:

            print('[Bob]: Start BB84 Protocol')
            BB84_key = B_party(len_BB84_key, Bob)
            print('[Bob]: End BB84 Protocol \n')
            print('===== END BB84 QKD Protocol ===== \n \n \n')
            
            # Bank (Bob) generates the EPR pair and sends
            # two qubits to Alice (A1 and A2)

            print('===== BEGIN intial GHZ generation and distribution ===== \n')
            print('[Bob]: Generates ' + str(n) + ' triplet GHZ states, every qubit of triplet denoted as B, A, C')
            qB_arr = []
            for i in range(0, n):
                qB = Bob.createEPR("Alice")
                qB_arr.append(qB)
            print('[Bob]: Sends ' +str(n) + ' A qubit group of GHZ state to Alice' )

            for i in range(0, n):
                qA = qubit(Bob)
                qB_arr[i].cnot(qA)
                Bob.sendQubit(qA,"Alice")
            print('[Bob]: Sends ' +str(n) + ' C qubit group of GHZ state to Alice' )

            # Bob now waits to receive the cheque from Charlie
            qC_arr = []
            for i in range(0, n):
                qC = Bob.recvQubit()
                qC_arr.append(qC)
            print('[Bob]: Receives ' +str(n) + ' C qubit group (The cheque) of GHZ states from Charlie \n' )

            print('===== END Submitting cheque to Bank ===== \n\n\n')
            print('===== BEGIN verification Process by Bank ===== \n')

            # Bob performs local computation which comprises of
            # Error correction after the bell state measurement performed by Alice
            for i in range(0, n):
                qB_arr[i].H()
                bob_measurement = measure(Bob, qB_arr[i])
                if bob_measurement == 1:
                    qC_arr[i].Z()
            print('[Bob]: Performs some local corrections and measures B qubit group to collapse the state to just the C qubit group (cheque) \n')

            # Bob computes the quantum one way function using the unique key
            # which is obtained from the supplementary information with the cheque
            # like 'r', 'db_id' and 'M'
            # and then performs a SWAP test to see if the result of the quantum one
            # way function is same as the cheque.
            res_same = []
            print('[Bob]: Recreates the quantum one way function by using the supplementary information from the cheque like database id, amount of money and randomised salt parameter. \n')

            test_var = input("[Test]: Enter a fake check? (yes/no)")

            for i in range(0, n):
                # True state
                if test_var == 'no':
                    owf_bank_state = one_way_function(Bob,
                        BB84_key, cheque[i]['db_id'], cheque[i]['r'], cheque[i]['M'])
                elif (test_var == 'yes'):    
                    # Random state (with incorrect db_id)
                    owf_bank_state = one_way_function(Bob,
                       BB84_key, 231, cheque[i]['r'], cheque[i]['M'])

                m_same = swap_test(Bob, owf_bank_state, qC_arr[i])
                res_same.append(m_same)
            print('[Bob]: Performs a SWAP test between the cheque and the state from quantum one way function' )
            print('[Bob]: Resulting array of SWAP test: ', res_same )

            corr_percent = (1-sum(res_same)/len(res_same))*100
            print("[Bob]: Correlation percentage between the two states is: " +
                str(corr_percent) + "%\n\n")

            threshold_constant_percent = (1 - (3/4)**n)*100
            print('[Bob]: Selects the threshold correlation percent:' + str(threshold_constant_percent) + "%")
            if (corr_percent > threshold_constant_percent):
                print ("[Bob]: Cheque is accepted")
            else:
                print("[Bob]: Cheque is aborted")
            print('===== END verification Process by Bank ===== \n\n')

def main():
    ThreadAlice().start()
    ThreadCharlie().start()
    ThreadBank().start()


if __name__ == "__main__":
    # execute only if run as a script
    main()
