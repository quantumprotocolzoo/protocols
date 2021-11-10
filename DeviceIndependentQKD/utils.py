#Define protocol parameters and utility functions
import math
import numpy as np
gamma = 0.2                     #Fraction of test rounds
w_exp = (2+math.sqrt(2))/ 4     #Expected winning probability of CHSH game in an honest implentations
del_est = 1e-3                  #Width of statistical interval for the Bell test
m = 1000                    #Number of blocks
s_max = math.ceil(1/gamma)      #Maximum rounds in a block
dist_AS = 4 / 1000              #Length of channel between Alice and Source
dist_AB = 400 / 1000            #Length of channel between Alice and Bob
dist_BS = 400 / 1000            #Length of channel between Bob and Source

#Establish all connections between the given nodes and the source
def set_up_network(alice,bob,source,channel1,channel2,channel3,qchannel1,qchannel2):
    
    #Set up ports
    alice.add_ports(['cout_source','cout_bob','cin_bob','qin_source'])
    bob.add_ports(['cout_alice','cin_alice','qin_source'])

    #Connect nodes to channels
    #Connect all of Alice's ports
    alice.ports['cout_source'].connect(channel1.ports['send'])  
    alice.ports['cout_bob'].connect(channel2.ports['send'])
    alice.ports['cin_bob'].connect(channel3.ports['recv'])
    alice.ports['qin_source'].connect(qchannel1.ports['recv'])

    #Connect all of Bob's ports
    bob.ports['cout_alice'].connect(channel3.ports['send'])
    bob.ports['cin_alice'].connect(channel2.ports['recv'])
    bob.ports['qin_source'].connect(qchannel2.ports['recv'])

    #Connect all of the EPR Source's ports
    source.ports['qout0'].connect(qchannel1.ports['send'])
    source.ports['qout1'].connect(qchannel2.ports['send'])
    source.ports['trigger'].connect(channel1.ports['recv'])


def random_bit(gamma):
    return np.random.choice([0,1], p = [1 - gamma, gamma])