import json
import sys

from collections import Iterable
from copy import deepcopy
from itertools import chain

from cqc.pythonLib import CQCConnection #only for testing in main

def _convert_gate_h(q1, q2, qubit_count):
    new_qubit = qubit_count + 1
    qubits = [[q1, q1, new_qubit], [new_qubit, 0, 0]]
    gates = ["E", "M", "X"]
    conditions = [0, 0, q1]
    return gates, qubits, conditions, new_qubit


def _convert_gate_cz(q1, q2, qubit_count):
    qubits = [[q1], [q2]]
    gates = ["E"]
    conditions = [0]
    return gates, qubits, conditions, qubit_count


def _convert_gate_x(q1, q2, qubit_count):
    qubits = [[q1], [0]]
    gates = ["X"]
    conditions = [0]
    return gates, qubits, conditions, qubit_count


def _convert_gate_z(q1, q2, qubit_count):
    qubits = [[q1], [0]]
    gates = ["Z"]
    conditions = [0]
    return gates, qubits, conditions, qubit_count

def _convert_gate_j(q1, q2, qubit_count, angle):
    new_qubit = qubit_count + 1
    qubits = [[q1, q1, new_qubit], [new_qubit, 0, 0]]
    gates = ["E","M","X"]
    conditions = [0, -angle%256, q1] 
    return gates, qubits, conditions, new_qubit


def _replace_qubit(qubits, old, new):
    qubits = deepcopy(qubits)
    for i, qubits_list in enumerate(qubits):
        for j, qubit in enumerate(qubits_list):
            if qubit == old:
                qubits[i][j] = new
    #print("replace new {} old {}".format(new,old))
    return qubits


def _convert_to_measurements(obj, gates, qubits, qubit_count, angles,qout_idx,qout_init,qout_final):
    if len(gates) == 0:
        for i in range(len(qout_idx)):
            qout_final[qout_init[i]-1]=qout_idx[i]
        #print("qout_final {}".format(qout_final))
        return obj

    gate = gates.pop(0)
    q1 = qubits[0].pop(0)
    q2 = qubits[1].pop(0)

    
    if gate == "H":
        new_gates, new_qubits, new_conditions, new_qubit_count = _convert_gate_h(
            q1, q2, qubit_count
        )
        if new_qubit_count != qubit_count:
            qubits = _replace_qubit(qubits, q1, new_qubit_count)
            qout_idx[qout_idx.index(q1)] = new_qubit_count
            qubit_count = new_qubit_count
            #print("qout_idx {}".format(qout_idx))
    elif gate == "CZ":
        new_gates, new_qubits, new_conditions, new_qubit_count = _convert_gate_cz(
            q1, q2, qubit_count
        )
    elif gate == "X":
        new_gates, new_qubits, new_conditions, new_qubit_count = _convert_gate_x(
            q1, q2, qubit_count
        )
    elif gate == "Z":
        new_gates, new_qubits, new_conditions, new_qubit_count = _convert_gate_z(
            q1, q2, qubit_count
        )
    elif gate == "J":
        angle = angles.pop(0)
        new_gates, new_qubits, new_conditions, new_qubit_count = _convert_gate_j(
            q1, q2, qubit_count,angle
        )
        if new_qubit_count != qubit_count:
            qubits = _replace_qubit(qubits, q1, new_qubit_count)
            qout_idx[qout_idx.index(q1)] = new_qubit_count
            qubit_count = new_qubit_count
            #print("qout_idx {}".format(qout_idx))
    elif gate == "CX":
        # Defer conversion to next iterations
        gates = ["H", "CZ", "H"] + gates
        qubits[0] = [q2, q1, q2] + qubits[0]
        qubits[1] = [0, q2, 0] + qubits[1]

        new_gates = []
        new_conditions = []
        new_qubits = [[], []]

    elif (gate == "T") | (gate == "R_Z"):
        # Defer conversion to next iterations
        gates = ["J", "H"] + gates
        qubits[0] = [q1, q1] + qubits[0]
        qubits[1] = [0, 0] + qubits[1]

        new_gates = []
        new_conditions = []
        new_qubits = [[], []]

    elif gate == "R_X":
        # Defer conversion to next iterations
        gates = ["H", "J"] + gates
        qubits[0] = [q1, q1] + qubits[0]
        qubits[1] = [0, 0] + qubits[1]

        new_gates = []
        new_conditions = []
        new_qubits = [[], []]


    else:
        print("ERROR {}".format(gate))
        sys.exit(1)


    obj["gates"] += new_gates
    obj["qubits"][0] += new_qubits[0]
    obj["qubits"][1] += new_qubits[1]
    obj["conditions"] += new_conditions
    # obj["angles"] += new_angles
    obj["qout_idx"] = qout_idx
    obj["qout_init"] = qout_init
    obj["qout_final"] = qout_final

    return _convert_to_measurements(obj, gates, qubits, qubit_count, angles, qout_idx, qout_init, qout_final)


def convert_to_measurements(gates, qubits, qubit_count, angles,qout_idx,qout_init,qout_final):
    empty = {"gates": [], "qubits": [[], []], "conditions": [], "angles": [], "qout_idx": [], "qout_init": [], "qout_final": []}
    return _convert_to_measurements(empty, gates, qubits, qubit_count, angles, qout_idx, qout_init, qout_final)


def load_circuit(path):
    with open(path, "r") as circ:
        circuit = json.load(circ)
    nGates = len(circuit["gates"])
    gates = []
    qubits = []
    qubits_1 = []
    qubits_2 = []
    qout_idx = []
    angles = []
    for g in range(0, nGates):
        qubits = qubits + circuit["gates"][g]["qbits"]
        #Warning, qubits are reading in undertermined order.
        qubits_1 = qubits_1 + [int(circuit["gates"][g]["qbits"][0])]
        if len(circuit["gates"][g]["qbits"]) == 1:
            qubits_2 = qubits_2 + [0]
        else:
            qubits_2 = qubits_2 + [int(circuit["gates"][g]["qbits"][1])]  
        gates = gates + [circuit["gates"][g]["type"]]
        if (gates[g] == 'R_Z') | (gates[g] == 'R_X'):
            angles = angles + [int(circuit["gates"][g]["angle"])]
        elif gates[g] == 'T' :
            angles = angles + [32]
    nqbits = len(set(qubits))
    qout_idx = list(map(int, set(qubits)))
    qout_init = list(map(int, set(qubits)))
    qout_final = [-1]*len(qout_idx)
    return gates, [qubits_1, qubits_2], nqbits, angles, qout_idx, qout_init, qout_final


def load_and_convert_circuit(path):
    circuit = load_circuit(path)
    #print("circuit={}".format(circuit))
    return convert_to_measurements(*circuit)


if __name__ == "__main__":
    result = load_and_convert_circuit("./circuits/circuitCNOT.json")
    gates = result["gates"]
    qubits = result["qubits"]
    conditions = result["conditions"]
    qout_idx = result["qout_idx"]
    qout_init = result["qout_init"]
    qout_final = result["qout_final"]    
    print("gates     :  {}".format(", ".join(gates)))
    print("qubits1   : {}".format(qubits[0]))
    print("qubits2   : {}".format(qubits[1]))
    print("conditions: {}".format(conditions))
    print("qout_idx: {}".format(qout_idx))
    print("qout_init: {}".format(qout_init))
    print("qout_final {}".format(qout_final))