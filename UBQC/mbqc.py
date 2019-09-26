import numpy as np, random, sys
from pathlib import Path

from ubqc.angle import measure_angle2

#only for testing with maibn
from cqc.pythonLib import CQCConnection, qubit

#only for mbqc function :
from ubqc.flow import circuit_file_to_flow, count_qubits_in_sequence


def mbqc(node, circuit, input_qubits):
	"""runs a given circuit using measurement based quantum computing

	:node: CQCConnection
	:circuit: path to circuit json file
	:input_qubits: list of input qubits on which the circuit will run. Must belong to node

	:return: list of output qubits
	"""

	seq_out = circuit_file_to_flow(str(circuit))
	nQubits = count_qubits_in_sequence(seq_out)

	E1=[]
	E2=[]

	for s in seq_out:
		#s.printinfo()
		if s.type=="E":
			E1.append(s.qubits[0])
			E2.append(s.qubits[1])
		
	outcome = nQubits * [-1]	# Outcome of each qubit measurement will be stored in this outcome list

	# generate the rest of the qubits for the graph state
	qubits = []
	for i in range(nQubits):
		if (i < len(input_qubits)):
			qubits.append(input_qubits[i])
		else:
			q = qubit(node)
			q.H() #|+> state
			qubits.append(q)

	# entangle all the qubits
	for i,j in zip(E1,E2):
		qubits[i-1].cphase(qubits[j-1])

	# run the measurements and corrections
	for s in seq_out:
		if s.type=='E':
			continue
		else:
			q = qubits[s.qubit-1]
		if s.type=='M':
			angle = measure_angle2(s, outcome, 0)
			q.rot_Z(-int(angle)%256)
			q.rot_Y(256-64)	# to make the measurement along in the |+> |-> basis
			outcome[s.qubit-1] = qubits[s.qubit-1].measure()
		elif s.type=='Z':
			if (s.power_idx == 0):
				q.Z()
			elif outcome[s.power_idx-1]==1:
				q.Z()
		elif s.type=='X':
			if (s.power_idx == 0):
				q.X()
			elif outcome[s.power_idx-1]==1:
				q.X()
	
	print(outcome)
	output_qubits = [qubits[i] for i,n in enumerate(outcome) if n==-1]	# get the qubits which have not been measured
	return output_qubits
		
def measure_mbqc(seq_out, nQubits, qubits):

	outcome = nQubits * [-1]

	for s in seq_out:
		if s.type=='E':
			continue
		else:
			q = qubits[s.qubit-1]
		if s.type=='M':
			angle = measure_angle2(s, outcome, 0)
			#print("angle = %d " % angle)
			q.rot_Z(-int(angle)%256)
			q.rot_Y(256-64)	# to make the measurement along in the |+> |-> basis
			outcome[s.qubit-1] = qubits[s.qubit-1].measure()
		elif s.type=='Z':
			if (s.power_idx == 0):
				q.Z()
			elif outcome[s.power_idx-1]==1:
				q.Z()
		elif s.type=='X':
			if (s.power_idx == 0):
				q.X()
			elif outcome[s.power_idx-1]==1:
				q.X()
	
	#print(outcome)
	output_qubits = [qubits[i] for i,n in enumerate(outcome) if n==-1]	# get the qubits which have not been measured
	output_idx = [i for i,n in enumerate(outcome) if n==-1] # get the index, used only for updating the graph. 
	return output_qubits, output_idx




if __name__ == "__main__":

	for i in range(10):
		with CQCConnection("Alice") as Alice:
			
			# generate the input qubits for the circuit
			q1 = qubit(Alice)
			q2 = qubit(Alice)
			q1.H()
			q2.X()
			
			#out = mbqc(Alice, "../ubqc/circuits/CNOT.json", [q1, q2])
			#out = mbqc(Alice, "../ubqc/circuits/circuitRZ.json", [q1, q2])
			out = mbqc(Alice, "../ubqc/circuits/circuit1.json", [q1,q2])

			# measure the output qubits
			final_result = []
			for q in out:
				#q.rot_Z(32)
				#q.H()
				final_result.append(q.measure())
			
			print('MBQC outcome:', final_result)
			Alice.close()




