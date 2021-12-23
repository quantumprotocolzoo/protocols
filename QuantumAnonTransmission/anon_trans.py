import netsquid as ns
import numpy as np
import sys
from anon_utils import *

#Default size of network, sender, receiver, quantum message
num_nodes = 5
sender_id = 0
dest_id = 4
message_state = ns.y0


if(len(sys.argv) == 6):
    num_nodes = int(sys.argv[1])
    sender_id = int(sys.argv[2])
    dest_id = int(sys.argv[3])
    alpha = complex(sys.argv[4])
    beta = complex(sys.argv[5])
    message_state = np.array([alpha,beta])
    state_norm = np.sqrt(pow(abs(alpha),2)+pow(abs(beta),2))
    message_state /= state_norm

else:
    print('Simulating with default values')

print('Number of nodes:',num_nodes)
print('Sender id: \t',sender_id)
print('Receiver id: \t',dest_id)
print('State to be transmitted:',message_state)
print('\nStarting simulation\n===================\n')


#Assign message state to qubit
message_qubit = ns.qubits.create_qubits(num_qubits = 1, no_state = True)[0]
ns.qubits.assign_qstate(message_qubit, message_state)


##Setup network            
nodes = setup_network(num_nodes)
nodes[sender_id].send(dest_id,message_qubit)
nodes[dest_id].receive()


#Start simulation
for i in range(num_nodes):
    nodes[i].start()


run_stats = ns.sim_run(duration = 1600)
#print(run_stats)
