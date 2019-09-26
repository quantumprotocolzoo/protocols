#use setting.json
from projectq import MainEngine
from projectq.backends import CircuitDrawer
from projectq.ops import H, CNOT, Measure, X, Z, CZ 
import json

def apply_gate(gate,qubits,b,i):
	if gate == "H":
		H | b[qubits[0][i]-1]
	elif gate == "X":
		X | b[qubits[0][i]-1]
	elif gate == "Z":
		Z | b[qubits[0][i]-1]
	elif gate == "CX":
		CNOT | (b[qubits[0][i]-1], b[qubits[1][i]-1])
	elif gate == "CZ":
		CZ | (b[qubits[0][i]-1], b[qubits[1][i]-1])
	return b
	        


def load_circuit(path):
    with open(path, "r") as circ:
        circuit = json.load(circ)
    nGates = len(circuit["gates"])
    gates = []
    qubits = []
    qubits_1 = []
    qubits_2 = []
    angles = []
    for g in range(0, nGates):
        qubits = qubits + circuit["gates"][g]["qbits"]
        qubits_1 = qubits_1 + [int(circuit["gates"][g]["qbits"][0])]
        if len(circuit["gates"][g]["qbits"]) == 1:
            qubits_2 = qubits_2 + [0]
        else:
            qubits_2 = qubits_2 + [int(circuit["gates"][g]["qbits"][1])]
        gates = gates + [circuit["gates"][g]["type"]]
        if gates[g] == 'T' :
            angles = angles + [32]
        if gates[g] == 'R_Z':
            angles = angles + [int(circuit["gates"][g]["angle"])]

    #print("qubits {}".format(qubits))
    nqbits = len(set(qubits))
    return gates, [qubits_1, qubits_2], nqbits, angles

def create_circuit(eng,path):
	result = load_circuit(path)
	gates = result[0]
	#print("gates = {} ".format(gates))
	qubits = result[1]
	#print("qubits = {} ".format(qubits))
	nqbits = result[2]
	angles = result[3]

	b = []
	for i in range(nqbits):
		q = eng.allocate_qubit()
		b.append(q)
	

	ngates = len(gates)
	for i in range(ngates):
		if qubits[1][i] != 0:
			apply_gate(gates[i],qubits,b,i)
		else :
			apply_gate(gates[i],qubits,b,i)

	return b



# create a main compiler engine
def create_eng(path):
	drawing_engine = CircuitDrawer()
	eng = MainEngine(drawing_engine)

	create_circuit(eng,path)

	eng.flush()
	with open('circuit.tex', 'w') as f:
    	#print >> f, 'Filename:', filename  # Python 2.x
    	#print('Filename:', filename, file=f)  # Python 3.x
		print(drawing_engine.get_latex(), file=f)

if __name__ == "__main__":
	path = "../ubqc/circuits/circuit9.json"
	create_eng(path)