import netsquid as ns
from netsquid.nodes import Node, DirectConnection
from netsquid.components import QuantumChannel, ClassicalChannel
from netsquid.components.qsource import QSource, SourceStatus
from netsquid.protocols import NodeProtocol
from netsquid.components.models.delaymodels import FibreDelayModel, FixedDelayModel
from netsquid.qubits.state_sampler import StateSampler
import netsquid.qubits.ketstates as ks 

from utils import *
import numpy as np

#Define protocol for Alice
class AliceProtocol(NodeProtocol):
    def __init__(self,node):
        super().__init__(node)
        self.key = ''
        self.n = 0

    #Protocol definition starts here
    def run(self):
        T = []
        X = []
        A = []
        observables = [ns.Z,ns.X]
        ind = -1
        for j in range(m):
            #For every block      
            i = 0
            while(i <= s_max):
                #For every round in a block  
                i += 1
                self.node.ports['cout_source'].tx_output('trigger source')  #Ask source to generate EPR Pair
                yield self.await_port_input(self.node.ports['qin_source'])  #Wait for qubit from source
                
                message = self.node.ports['qin_source'].rx_input()
                qubit = message.items[0]    #Extract qubit received from source

                T.append(random_bit(gamma))  #Randomly decide if current round is a test round or not
                ind+=1

                self.node.ports['cout_bob'].tx_output(T[ind])   #Tell Bob the value of T[ind]

                if(T[ind] == 0):
                    #If not a test round
                    X.append(0) #Measure in Z-basis
                else:
                    #If test round
                    X.append(np.random.randint(2))  #Measure randomly in Z or X basis

                meas,p = ns.qubits.measure(qubit, observable = observables[X[ind]])  #Measure in basis determined by X[ind]
                A.append(meas)  #Store measurement result
                if(T[ind] == 1):
                    i = s_max+1

        #Begin Parameter Estimation
        self.n = len(T)
        
        for i in range(self.n):
            if(T[i] == 0):
                self.key += str(A[i])    #If not a test round, add result to key
            else:
                yield self.await_port_input(self.node.ports['cin_bob']) #Wait for Bob's request to send test data

                self.node.ports['cout_bob'].tx_output((A[i],X[i])) #Send test outcome and basis to Bob
        
        yield self.await_port_input(self.node.ports['cin_bob'])    #Wait for Bob's parameter estimation result
        message = self.node.ports['cin_bob'].rx_input()
        result = message.items[0]
        
        if(result == 0):
            print('Alice Aborting')
            key = ''
        else:
            print('Alice: Key distribution successful')

#Define protocol for Bob
class BobProtocol(NodeProtocol):
    def __init__(self,node):
        super().__init__(node)
        self.key = ''

    #Protocol definition starts here
    def run(self):
        T = []
        Y = []
        B = []
        H = (ns.Z+ns.X)/np.sqrt(2)
        H_ = (ns.Z-ns.X)/np.sqrt(2)
        observables = [H,H_,ns.Z]
        ind = -1
        for j in range(m):
            #For every block      
            i = 0
            while(i <= s_max):
                #For every round in a block  
                i += 1
                yield self.await_port_input(self.node.ports['qin_source'])  #Wait for qubit from source
                
                message = self.node.ports['qin_source'].rx_input()
                qubit = message.items[0]    #Extract qubit received from source

                yield self.await_port_input(self.node.ports['cin_alice'])   #Wait for T value from Alice
                message = self.node.ports['cin_alice'].rx_input()
                T.append(message.items[0])  #Decide if current round is a test round or not
                ind+=1


                if(T[ind] == 0):
                    #If not a test round
                    Y.append(2) #Measure in Z-basis
                else:
                    #If test round
                    Y.append(np.random.randint(2))  #Measure randomly in H or H_ basis

                meas,p = ns.qubits.measure(qubit, observable = observables[Y[ind]])  #Measure in basis determined by X[ind]
                B.append(meas)  #Store measurement result
                if(T[ind] == 1):
                    i = s_max+1

        #Begin Parameter Estimation
        print('Bob : Starting parameter estimation')
        n = len(T)  #Number of rounds
        C = []      #Test results for each round
    
        for i in range(n):
            
            if(T[i] == 0):
                self.key += str(B[i])    #If not a test round, add measurement result to key
                C.append('-')
            else:
                self.node.ports['cout_alice'].tx_output('READY')               #Ask Alice to send next test data
                yield self.await_port_input(self.node.ports['cin_alice'])   #Wait for test outcome and basis from Alice
                message = self.node.ports['cin_alice'].rx_input()
                a,x = message.items[0]
                #Calculate CHSH result
                if(a^B[i] == x*Y[i]):
                    C.append('1')
                else:
                    C.append('0')

        #Calculate successful test rounds
        sum = C.count('1')
        threshold = m * (w_exp - del_est) * (1 - (1-gamma)**s_max)
        print('Bob : Observed CHSH wins - ' + str(sum))
        print('Bob : Threshold CHSH wins - '+str(threshold))
        
        result = 1
        if(sum < threshold):
            result = 0
        else:
            result = 1
        self.node.ports['cout_alice'].tx_output(result)        
       
        if(result == 0):
            print('Bob Aborting')
            key = ''
        else:
            print('Bob: Key distribution successful ')

        
    
#Define nodes
alice_node = Node(name="Alice")
bob_node = Node(name="Bob")

#Define EPR pair source
state_sampler = StateSampler([ks.b00],[1.0])
qsource = QSource(name = "EPR Source", state_sampler = state_sampler, status = SourceStatus.EXTERNAL,num_ports = 2)

#Define delay model
delay_model = FibreDelayModel()
    
#Define classical channels
channel_A2S = ClassicalChannel("A_to_S",length = dist_AS, models={"delay_model":delay_model})
channel_A2B = ClassicalChannel("A_to_B",length = dist_AB, models={"delay_model":delay_model})
channel_B2A = ClassicalChannel("B_to_A",length = dist_AB, models={"delay_model":delay_model})
    
#Define Quantum Channels
qchannel_A = QuantumChannel(name="qchannel[S to A]",length = dist_AS, models={"delay_model":delay_model})
qchannel_B = QuantumChannel(name="qchannel[S to B]",length = dist_BS, models={"delay_model":delay_model})

#Connect nodes to channels
set_up_network(alice_node,bob_node,qsource,channel_A2S,channel_A2B,channel_B2A,qchannel_A,qchannel_B)

#Create protocol objects
alice_protocol = AliceProtocol(alice_node)
bob_protocol = BobProtocol(bob_node)

#Start simulation
alice_protocol.start()
bob_protocol.start()



run_stats = ns.sim_run()

#Verify protocol correctness
assert alice_protocol.key == bob_protocol.key

print(str(len(alice_protocol.key)) + '-bit key established')
print(str(alice_protocol.n) + ' rounds were needed')

#print(run_stats)
#View simulation statistics    