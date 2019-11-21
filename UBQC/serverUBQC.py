import sys
import json
#import struct
import time
import pickle
import argparse
from argparse import RawTextHelpFormatter
import matplotlib.pyplot as plt
from matplotlib.pyplot import ion,show
from graph import draw_graph_pos, update_graph
from cqc.pythonLib import CQCConnection, qubit


parser=argparse.ArgumentParser(
#    description='''Description. '''#,
#    epilog="""All's well that ends well."""
#)
    description='''Description.\nexample : python serverUBQC.py -d''',
    formatter_class=RawTextHelpFormatter
    )
parser.add_argument('-d','--draw', action="store_true", help='draw the graph')
args=parser.parse_args()


qubits = []
num_measurements = 4
outcome = []

client_name = "Alice"

with CQCConnection("Bob") as Server:
    # Client first defines number of qubits needed for their circuit
    nQubits = Server.recvClassical()
    nQubits = int.from_bytes(nQubits, byteorder="little")
    print("Server Received (classical): Create {} qubits".format(nQubits))

    # We need to receive all qubits from client
    for i in range(nQubits):
        qubits.append(Server.recvQubit())
    print("Server Received (quntum): qubits received")

    # Client next defines the number of measurments to be performed
    nMeasurement = Server.recvClassical()
    nMeasurement = int.from_bytes(nMeasurement, byteorder="little")
    print(
        "Server Received (classical): Client asking to perform {} measurements".format(
            nMeasurement
        )
    )

    # First step of MBQC is entangling qubits into a graph state
    E = []
    E1 = Server.recvClassical()
    print("Server Received (classical): List of 1st Qubits to Entangle".format(nQubits))
    E2 = Server.recvClassical()
    print("Server Received (classical): List of 2nd Qubits to Entangle".format(nQubits))
    print("Server Entangling...")
    for i, j in zip(E1, E2):
        qubit_i = qubits[i - 1]
        qubit_j = qubits[j - 1]
        qubit_i.cphase(qubit_j)
        E.append([i,j])
        print("entg qubit {} with qubit {}".format(i, j))
    print("E= {}".format(E))

    if(args.draw):
        G1 = draw_graph_pos(E,nQubits-nMeasurement,nQubits)

    # Server is ready to measure!
    print("Server Measuring...")
    qout_idx = list(range(nQubits))
    #print("{} {}".format(qout_idx,nQubits))
    for i in range(nMeasurement):
        # Each measurement has has a qubit index (between 0 and nQubits)
        qubit_n = int.from_bytes(Server.recvClassical(), "little")
        # Each measurement has an angle to measure in degrees
        angle = int.from_bytes(Server.recvClassical(), "little")
        qout_idx.remove(qubit_n-1)
        #print("{}".format(qout_idx))
        print("Server Measuring qubit {} using angle {}".format(qubit_n, angle))
        #qubits[qubit_n-1].rot_Z(angle)
        qubits[qubit_n-1].rot_Z(-int(angle)%256)
        qubits[qubit_n-1].rot_Y(256-64) # to make the measurement along in the |+> |-> basis
        m = qubits[qubit_n-1].measure()

        time.sleep(0.1)
        print("Server Sending (classical): result of measurement {}".format(m))
        Server.sendClassical(client_name, m)

    for i in range(nQubits-nMeasurement):
        print("Server Sending (quantum): qubit {}".format(qout_idx[i]+1))
        Server.sendQubit(qubits[qout_idx[i]], client_name)
        recv_data = Server.recvClassical() #recv ok from the client
        data = pickle.loads(recv_data)
        print("message = {} ".format(data))

    if(args.draw):
        update_graph(G1[0],G1[1],G1[2],qout_idx)
        plt.show()

    sys.exit(0)
