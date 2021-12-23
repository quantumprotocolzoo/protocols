import netsquid as ns
from netsquid.nodes import Node, DirectConnection
from netsquid.components import QuantumChannel, ClassicalChannel
from netsquid.components.qsource import QSource, SourceStatus
from netsquid.protocols import NodeProtocol
from netsquid.components.models.delaymodels import FibreDelayModel, FixedDelayModel
from netsquid.qubits.state_sampler import StateSampler
import numpy as np


class GHZ_QAT_Protocol(NodeProtocol):
    def __init__(self,n,id,node):
        super().__init__(node)
        self.id = id                #Node id
        self.n = n                  #Number of nodes in the network
        self.sender = False
        self.receiver = False

    def send(self,dest,message_qubit):
        assert self.receiver == False and self.id != dest
        self.sender = True
        self.dest = dest
        self.message_qubit = message_qubit
        
    def receive(self):
        assert self.sender == False
        self.receiver = True

    def run(self):
        #Anonymously distribute an EPR pair between sender and receiver

        #Get shared GHZ state
        yield self.await_port_input(self.node.ports['qin'])
        message = self.node.ports['qin'].rx_input()
        tel_qubit = message.items[0]

        m = 0
        if(not(self.sender or self.receiver)):
        #If not sender or receiver, get measurement outcome
            ns.qubits.operate(tel_qubit,ns.H)
            m,p = ns.qubits.measure(tel_qubit, discard = True)
        else:
        #If sender or receiver, get random bit
            m = np.random.randint(2)

        if(self.sender and m == 1):
        #If sender, apply necessary operation
            ns.qubits.operate(tel_qubit,ns.Z)

        counter = 0
        for i in range(self.n):
            if(i == self.id):
            #If my turn, broadcast m
                self.broadcast(m)
            else:
            #If not my turn, receive broadcast
                address = 'cin'+str(i)
                yield self.await_port_input(self.node.ports[address])
                message = self.node.ports[address].rx_input().items[0]
                #Receiver updates counter mod 2
                counter ^= message

        if(self.receiver and counter == 1):
        #If receiver, apply necessary operation
            ns.qubits.operate(tel_qubit,ns.Z)

        #Entanglement established anonymously
        #Now, we use the EPR state created to anonymously teleport the message state

        tel_m = [0,0]
        if(self.sender):
            #If sender, apply teleportation operations
            ns.qubits.operate([self.message_qubit,tel_qubit],ns.CNOT)
            ns.qubits.operate(self.message_qubit,ns.H)
            tel_m[0],p = ns.qubits.measure(self.message_qubit, discard = True)
            tel_m[1],p = ns.qubits.measure(tel_qubit, discard = True)

        for k in range(2):
            #Anonymously transmit each teleportation bit

            #Wait for GHZ state
            yield self.await_port_input(self.node.ports['qin'])
            message = self.node.ports['qin'].rx_input()
            qubit = message.items[0]
            
            #Sender operations for anonymous bit transmission
            if(self.sender and tel_m[k] == 1):                
                ns.qubits.operate(qubit,ns.Z)
            
            #Anonymous bit transmission operations
            ns.qubits.operate(qubit,ns.H)
            m,p = ns.qubits.measure(qubit)

            counter = m
            for i in range(self.n):
                if(i == self.id):
                #If my turn, broadcast m
                   self.broadcast(m)
                else:
                #If not my turn, receive broadcast
                    address = 'cin'+str(i)
                    yield self.await_port_input(self.node.ports[address])
                    broadcast_in = self.node.ports[address].rx_input().items[0]
                    #Receiver updates counter mod 2
                    counter ^= broadcast_in
            tel_m[k] = counter

        if(self.receiver):
            #Receiver applies teleportation operations
            if(tel_m[1] == 1):
                ns.qubits.operate(tel_qubit,ns.X)
            if(tel_m[0] == 1):
                ns.qubits.operate(tel_qubit,ns.Z)

            #Message qubit has now been received
            print('Node '+ str(self.id) + ": Received quantum message - \n" + str(tel_qubit.qstate.qrepr))
            ns.qubits.discard(tel_qubit)

        #End of protocol

    def broadcast(self,message):
        for i in range(self.n):
            if(i == self.id):
                continue
            address = 'cout'+str(i)
            self.node.ports[address].tx_output(message)

def setup_network(num_nodes):
    #Define nodes      
    assert num_nodes >= 2
    node = []
    for i in range(num_nodes):
        node.append(Node(name = str(i)))

    #Prepare GHZ state source
    q = ns.qubits.create_qubits(num_qubits = num_nodes)
    ns.qubits.operate(q[0],ns.H)
    for i in range(1,num_nodes):
        ns.qubits.operate([q[0],q[i]],ns.CNOT)
    state = q[0].qstate.qrepr
    state_sampler = StateSampler([state],[1.0])
    source_delay = 300
    qsource = QSource(name = "GHZ Source", state_sampler = state_sampler, status = SourceStatus.INTERNAL,num_ports = num_nodes,timing_model = FixedDelayModel(source_delay))

    #Create classical channels
    channel = []
    distance = 4 / 1000
    delay_model = FibreDelayModel()
    for i in range(num_nodes):
        empty_list = []
        channel.append(empty_list)
        for j in range(num_nodes):
            if(i == j):
                channel[i].append(None)
            else:
                name = str(i) + 'to' + str(j)
                channel[i].append(ClassicalChannel(name, length = distance, models={"delay_model":delay_model}))

    #Add ports to nodes
    for i in range(num_nodes):
        for j in range(num_nodes):
            node[i].add_ports(['cout'+str(j),'cin'+str(j)]) 
        node[i].add_ports(['qin'])

    #Connect nodes to classical channels
    for i in range(num_nodes):
        for j in range(i):
            node[i].ports['cout'+str(j)].connect(channel[i][j].ports['send'])
            node[j].ports['cout'+str(i)].connect(channel[j][i].ports['send'])
            node[i].ports['cin'+str(j)].connect(channel[j][i].ports['recv'])
            node[j].ports['cin'+str(i)].connect(channel[i][j].ports['recv'])

    #Create quantum channels
    qchannel = [QuantumChannel('QChannel'+str(i), length = distance) for i in range(num_nodes)]

    #Connect GHZ source to nodes
    for i in range(num_nodes):
        qsource.ports['qout'+str(i)].connect(qchannel[i].ports['send'])
        node[i].ports['qin'].connect(qchannel[i].ports['recv'])


    #Bind protocols to nodes
    protocol = []
    for i in range(num_nodes):
        protocol.append(GHZ_QAT_Protocol(n = num_nodes,id = i,node = node[i]))

    return protocol
