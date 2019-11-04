import random
from pathlib import Path
import numpy as np
import pickle
import argparse
from argparse import RawTextHelpFormatter
from circuit_projetq import create_eng
import subprocess 
from measurement import load_circuit, convert_to_measurements
from flow import count_qubits_in_sequence, _measurement_dictionary_to_sequence, _construct_flow_from_sequence
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
    description='''Description.\nexample : python clientMBQC.py -c circuits/circuit7.json -d -i X,I -o I,H''',
    formatter_class=RawTextHelpFormatter)
parser.add_argument('-d','--draw', action="store_true", help='draw the circuit')
parser.add_argument('-c','--circuit', type=str, help='choose a particular circuit in circuits', default="")
parser.add_argument('-i','--input', type=str, help='choose gates to apply on input states, default |0>. can be Pauli,rot_Pauli(angle),H,K,T.', default="")
parser.add_argument('-o','--output', type=str, help='choose gates to apply before measurement in Z. can be Pauli,rot_Pauli(angle),H,K,T.', default="")
args=parser.parse_args()


if args.input:
    input_gates = args.input.split(',')

if args.output:
    output_gates = args.output.split(',')

# Randomly select circuit from circuits directory
if not args.circuit:
    circuits_path = Path(".") / "circuits"
    circuit_file_paths = list(circuits_path.glob("*.json"))
    path = random.choice(circuit_file_paths)
else:
    path=args.circuit

# Load circuit given as a json file and convert to MBQC flow
print("load and convert {}".format(path))
circuit = load_circuit(path)
if(args.draw):
    create_eng(path)
    proc = subprocess.run("pdflatex circuit.tex > /dev/null", shell=True)
    proc = subprocess.run("evince circuit.pdf 2>/dev/null &",shell=True)
ninput = circuit[2]
result = convert_to_measurements(*circuit) 
qout_idx = result["qout_final"]
#print("qout_idx {}".format(qout_idx))
seq_in = _measurement_dictionary_to_sequence(result)
#for s in seq_in:
#    s.printinfo()
seq_out = _construct_flow_from_sequence(seq_in)


# Determine number of cubits our circuit needs
nQubits = count_qubits_in_sequence(seq_out)

# Initialize measurements count and entanglement lists
nMeasurement = 0
Edges = []

# We use the flow sequence to build entanglement lists and count measurements
for s in seq_out:
    #s.printinfo()
    if s.type == "E":
        Edges.append(s.qubits)

# Outcome of each qubit will be stored in this outcome list
outcome = nQubits * [-1]

with CQCConnection("Alice") as Alice:
    msg="OK"
    data_ok = pickle.dumps(msg)

    print("Client Sending: Number of qubits = {}".format(nQubits))
    Alice.sendClassical("Bob", nQubits)
    
    recv_data = Alice.recvClassical()
    data = pickle.loads(recv_data)
    if data != "OK": 
        print("message = {} ".format(data))

    print("Client Sending: Number of input qubits = {}".format(ninput))
    Alice.sendClassical("Bob", ninput) 

    recv_data = Alice.recvClassical()
    data = pickle.loads(recv_data)
    if data != "OK": 
        print("message = {} ".format(data))

    #time.sleep(1)
    print("Client Sending: seq_out")
    data = pickle.dumps(seq_out)
    Alice.sendClassical("Bob", data) 
    recv_data = Alice.recvClassical()
    data = pickle.loads(recv_data)
    if data != "OK": 
        print("message = {} ".format(data))


    qin = []
    for i in range(ninput):
        q = qubit(Alice)
        if args.input:
            U = input_gates[i]
            q = apply_singleU(U,q)
            print("apply {} to qubit {}".format(U,i))
        qin.append(q)

    
    for i in range(ninput):
        print("Client Sending: qubit {} ".format(i))
        Alice.sendQubit(qin[i],"Bob")
        recv_data = Alice.recvClassical()
        data = pickle.loads(recv_data)
        if data != "OK": 
            print("message = {} ".format(data))
   

   
    

    noutput = Alice.recvClassical()
    noutput = int.from_bytes(noutput, byteorder="little")
    print("Client Received: Number of output states = {}".format(noutput))
    if(noutput != len(qout_idx)):
    	print("unexpected number of output {}, expected {}".format(noutput,len(qout_idx)))


    qout = [-1]*len(qout_idx)
    qidx_sort = qout_idx[:]
    qidx_sort.sort()
    for i in range(noutput):
        q = Alice.recvQubit()
        Alice.sendClassical("Bob",data_ok)
        qout[qidx_sort.index(qout_idx[i])]=q

    meas = []
    for i in range(noutput): 
        if args.output:
            U = output_gates[i]
            print("apply {} to qubit {} sorting to {}".format(U,qout_idx[i],i))
            qout[i] = apply_singleU(U,qout[i])
        meas.append(qout[i].measure())     

    print("meas in Z basis = {}".format(meas))
    Alice.close()

if args.draw:
    subprocess.run("rm -f circuit*.aux",shell=True) 
    subprocess.run("rm -f circuit*.log",shell=True) 
    subprocess.run("rm -f circuit*.tex",shell=True) 
    subprocess.run("rm -f circuit*.pdf",shell=True) 