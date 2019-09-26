import random
import sys
import time
from pathlib import Path
import pickle
import numpy as np
import argparse
from argparse import RawTextHelpFormatter

#to create the cricuit:
import subprocess
from circuit_projetq import create_eng
#to compute graph measurement and angle pattern
from flow import circuit_file_to_flow, count_qubits_in_sequence
from angle import measure_angle2
#to simulate with simualqron:
from cqc.pythonLib import CQCConnection, qubit


def apply_singleU(U,q):
    if U=='X':
        q.X()
    elif U=='Y':
        q.Y()
    elif U=='Z':
        q.Z()
    elif U=='H':
        q.H()
    elif U=='K':
        q.K()
    elif U=='T':
        q.T()
    elif U=='rot_X':
        angle = input("angle ?")
        q.rot_X(int(angle))
    elif U=='rot_Y':
        angle = input("angle ?")
        q.rot_Y(int(angle))
    elif U=='rot_Z':
        angle = input("angle ?")
        q.rot_Z(int(angle))
    return q  



parser=argparse.ArgumentParser(
    description='''Description.\nexample : python clientUBQC.py -c circuits/circuit7.json -d -i Z,I -o I,H''',
    formatter_class=RawTextHelpFormatter)
parser.add_argument('-d','--draw', action="store_true", help='draw the circuit')
parser.add_argument('-c','--circuit', type=str, help='choose a particular circuit in ubqc/circuits', default="")
parser.add_argument('-i','--input', type=str, help='choose gates to apply on input states, default |+>. can be Pauli, rot_Pauli(angle),H,K,T.', default="")
parser.add_argument('-o','--output', type=str, help='choose gates to apply before measurement, default is Z. can be Pauli, rot_Pauli(angle),H,K,T.', default="")
args=parser.parse_args()


# Randomly select circuit from circuits directory
if not args.circuit:
    circuits_path = Path(".") / "circuits"
    circuit_file_paths = list(circuits_path.glob("*.json"))
    path = random.choice(circuit_file_paths)
else:
    path=args.circuit

if args.input:
    input_gates = args.input.split(',')

if args.output:
    output_gates = args.output.split(',')


print("Client Loading {}".format(path))
if(args.draw):
    create_eng(path)
    proc = subprocess.run("pdflatex circuit.tex > /dev/null", shell=True)
    proc = subprocess.run("evince circuit.pdf 2>/dev/null &",shell=True)

cftf = circuit_file_to_flow(path)
seq_out = cftf[0]

# Determine number of cubits our circuit needs
nQubits = count_qubits_in_sequence(seq_out)

# Output the index of output qubits in order they will appear
qout_idx = cftf[1]
#print("qout_final {}".format(qout_idx))

# Initialize measurements count and entanglement lists
nMeasurement = 0
E1 = []
E2 = []

# We use the flow sequence to build entanglemtn lists and count measurements
for s in seq_out:
    #s.printinfo()
    if s.type == "E":
        E1.append(s.qubits[0])
        E2.append(s.qubits[1])
    if s.type == "M":
        nMeasurement += 1
nInputs = nQubits - nMeasurement

# Outcome of each qubit will be stored in this outcome list
outcome = nQubits * [-1]

server_name = "Bob"

msg="OK"
data_ok = pickle.dumps(msg)

with CQCConnection("Alice") as client:

    qubits = []
    angles = []
    for i in range(0, nInputs):
        rand_angle = int(256 * random.random())
        angles.append(rand_angle)
        print("i = {} rand_ang = {}".format(i,angles[i]))
        q = qubit(client)
        q.rot_Y(64)  # |+> state
        if args.input:
            U = input_gates[i]
            q = apply_singleU(U,q)
            print("apply {} to qubit {}".format(U,i))
        q.rot_Z(rand_angle)
        qubits.append(q)
        
    for i in range(nInputs, nQubits):
        rand_angle = int(256 * random.random())
        angles.append(rand_angle)
        print("i = {} rand_ang = {}".format(i,angles[i]))
        q = qubit(client)
        q.rot_Y(64)  # |+> state
        q.rot_Z(rand_angle)
        qubits.append(q)

    print("Client Sending (classical): Create {} qubits".format(nQubits))
    client.sendClassical(server_name, nQubits)

    for i in range (0,nQubits):    
        print("Client Sending (quantum): qubit {}".format(i + 1))
        client.sendQubit(qubits[i], server_name)

    time.sleep(0.1)
    print("Client Sending (classical): Ask to perform {} measurements".format(nMeasurement))
    client.sendClassical(server_name, nMeasurement)
    time.sleep(0.1)
    print("Client Sending (classical): List of 1st Qubits to Entangle".format(nQubits))
    client.sendClassical(server_name, E1)
    time.sleep(0.1)
    print("Client Sending (classical): List of 2nd Qubits to Entangle".format(nQubits))
    client.sendClassical(server_name, E2)

    qout_idx2 = list(range(nQubits))
    for s in seq_out:
        if s.type == "M":
            # Which qubit are we measuring?
            qubit_n = s.qubit
            qout_idx2.remove(qubit_n-1)

            # What is the angle we wish to measure
            computation_angle = s.angle
            input_angle = angles[qubit_n-1]

            # Calculate the angle to send with randomisation applied
            r = np.round(random.random())
            #angle_to_send = measure_angle(qubit_n, seq_out, outcome, input_angle, computation_angle) + r * (np.pi)
            angle_to_send = (measure_angle2(s, outcome, input_angle) + r * 128) % 256 #PI = 128
            print("s.angle = {} outcome = {} input_angle = {} meas_ang2 = {} r = {} to_send = {}".format(s.angle,outcome,input_angle,measure_angle2(s, outcome, input_angle),r,angle_to_send))

            print("Client Sending (classical): ask to measure qubit {}".format(qubit_n))
            time.sleep(0.1)
            client.sendClassical(server_name, qubit_n)

            print(
                "Client Sending (classical): measurement angle {}".format(angle_to_send)
            )
            time.sleep(0.1)
            client.sendClassical(server_name, angle_to_send)

            m = int.from_bytes(client.recvClassical(), "little")
            print("Client Received: result {}".format(m))

            # We adjust for the randomness only we know we added
            if r == 1:
                outcome[qubit_n - 1] = 1 - m
                #outcome2[qubit_n - 1] = m

            else:
                outcome[qubit_n - 1] = m
                #outcome2[qubit_n - 1] = 1 - m


    #print("qout_idx2 {}".format(qout_idx2))

    #receiving and reordering output qubits
    print("Client Receiving output qubits")
    qout = [-1]*len(qout_idx)
    qidx_sort = qout_idx[:]
    qidx_sort.sort()
    noutput = len(qout_idx)
    for i in range(noutput):
        q = client.recvQubit()
        client.sendClassical(server_name,data_ok)
        print("Client Received: recv qubit {} sorting to {}".format(qout_idx2[i]+1,qidx_sort.index(qout_idx[i])))
        qout[qidx_sort.index(qout_idx[i])]=q


    print("Client applying correction") 
    for i in range(noutput):
        qout[i].rot_Z(-int(angles[qout_idx[i]-1])%256)
        print("apply rot_Z({}) on qubit {}".format(-int(angles[qout_idx[i]-1])%256,qout_idx[i]))

    for i in range(noutput):
        for s in seq_out:
            if s.type == "Z" and s.qubit == qout_idx[i] and outcome[s.power_idx-1] == 1: 
                qout[i].Z()
                print("apply Z dep : s = {} idx = {} on qubit {}".format(outcome[s.power_idx-1],s.power_idx,qout_idx[i]))   
            if s.type == "X" and s.qubit == qout_idx[i] and outcome[s.power_idx-1] == 1: 
                qout[i].X()
                print("apply X s = {} idx = {} on qubit {}".format(outcome[s.power_idx-1],s.power_idx,qout_idx[i]))

       
    meas = []
    print("number of output qubits : ",nQubits-nMeasurement)
    for i in range(nQubits-nMeasurement): 
        if args.output:
            U = output_gates[i]
            print("apply {} to qubit {} sorting to {}".format(U,qout_idx[i],i))
            qout[i] = apply_singleU(U,qout[i])
        meas.append(qout[i].measure())     

    # qout[i].rot_X(256-64)
    # meas.append(qout[i].measure())  
    # meas.append(qout[0].measure())
    # qout[1].H()
    # meas.append(qout[1].measure())
    # qout[0].X()
    # meas.append(qout[0].measure())
    # meas.append(qout[1].measure())

    print("meas in Z basis = {}".format(meas))
    client.close()
    if args.draw:
        subprocess.run("rm -f circuit*.aux",shell=True) 
        subprocess.run("rm -f circuit*.log",shell=True) 
        subprocess.run("rm -f circuit*.tex",shell=True) 
        subprocess.run("rm -f circuit*.pdf",shell=True) 

    sys.exit(0)

