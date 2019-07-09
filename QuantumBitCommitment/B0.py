import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from cqc.pythonLib import CQCConnection, qubit
from time import sleep

measurement = []
agent1_ = []
agent2_ = []
wait = 1

'''
In the prep_Bob function
commitmentment bit was produced as commitment
sent qubits from A0 were accepted and 
according to commitment applied H gate and 
measured and saved in measurement list.
Measurement list was sent B1 and B2
commitment bit was sent B1 and B2
'''

def prep_Bob():

    with CQCConnection("B0") as B0:
        commitment = randint(0,1)
        for i in range(10):
            q = B0.recvQubit()
           
            if commitment == 1:
               q.H()
            a = q.measure()
            measurement.append(a)
        print("qubit received")
        sleep(wait)
        B0.sendClassical("B1", measurement)
        print("a sent to B1")
        sleep(wait)
        B0.sendClassical("B2", measurement)
        print("a sent to B2")
        sleep(wait)
        B0.sendClassical("B1",commitment)  
        print("commitment sent to B1")
        sleep(wait)
        B0.sendClassical("B2",commitment)   
        print("commitment sent to B2")
       # print ("sended for Agent1:", agent1_)      
       # print ("sended for Agent2:", agent2_)    
        print ("HELLO2")       
if __name__ == "__main__":

    prep_Bob()
            
