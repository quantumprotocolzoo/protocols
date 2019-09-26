import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import ion,show
import pickle
import argparse
from argparse import RawTextHelpFormatter
from graph import draw_graph_pos, update_graph
from mbqc import measure_mbqc
from cqc.pythonLib import CQCConnection, qubit


parser=argparse.ArgumentParser(
#    description='''Description. '''#,
#    epilog="""All's well that ends well."""
#)
    description='''Description.\nexample : python serverMBQC.py -d''',
    formatter_class=RawTextHelpFormatter
    )
parser.add_argument('-d','--draw', action="store_true", help='draw the graph')
args=parser.parse_args()


with CQCConnection("Bob") as Bob:
    msg="OK"
    data_ok = pickle.dumps(msg)

    nQubits = Bob.recvClassical()
    nQubits = int.from_bytes(nQubits, byteorder="little")
    print("Bob Received: Number of qubits = {} ".format(nQubits))

    Bob.sendClassical("Alice", data_ok)

    ninput = Bob.recvClassical()
    ninput = int.from_bytes(ninput, byteorder="little")
    print("Bob Received: Number of input states = {}".format(ninput))

    Bob.sendClassical("Alice", data_ok)

    # #Edges = []
    # recvd_data = Bob.recvClassical()
    # Edges = pickle.loads(recvd_data)
    # print("Bob Received: Edges = {}".format(Edges))
    # recvd_data = Bob.recvClassical()
    # data = pickle.loads(recvd_data)
    # print("Bob Received: = {}".format(data))

    recvd_data = Bob.recvClassical()
    seq_out = pickle.loads(recvd_data)
    print("Server Received: seq_out")
    Bob.sendClassical("Alice", data_ok)

    Edges = []
    for s in seq_out:
        s.printinfo()
        if s.type == "E":
            Edges.append(s.qubits)

    print("E= {}".format(Edges))
    #print("Server receiving input states")
    qubits = []
    for i in range(ninput):
        q = Bob.recvQubit()
        Bob.sendClassical("Alice", data_ok)
        qubits.append(q)
        print("Server Received: qubit received.")


    print("Server creates graph state")
    for i in range(ninput,nQubits):
    	q = qubit(Bob)
    	q.H() #|+> state
    	qubits.append(q)   
    #qout_idx = list(range(nQubits))
    for E in Edges:
    	qubits[E[0]-1].cphase(qubits[E[1]-1])

    #Comment to not draw the graph
    if(args.draw):
        G1 = draw_graph_pos(Edges,ninput,nQubits)


    print("Server makes adaptive measurements and corrections")
    result = measure_mbqc(seq_out,nQubits,qubits)
    qout = result[0]
    #print("idx_output ",result[1])

    #comment to not draw/update the graph
    if(args.draw):
        idx_output = result[1]
        update_graph(G1[0],G1[1],G1[2],idx_output)

    noutput = len(qout)
    
    print("Server Sending: Number of output qubits = {}".format(noutput))
    Bob.sendClassical("Alice", noutput) 

    for q in qout: 
        Bob.sendQubit(q,"Alice")
        recvd_data = Bob.recvClassical()
        data = pickle.loads(recvd_data)
        if data != "OK": 
            print("Server received : {} ".format(data))

    if(args.draw): 
        plt.show()
    Bob.close()
