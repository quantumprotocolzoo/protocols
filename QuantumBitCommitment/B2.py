from cqc.pythonLib import CQCConnection, qubit
from time import sleep
received2 = []
wait = 1

'''
B2 accepts the knowledges from B0
and after waiting a specific time 
it sends knowledge(accepted measurement list 
and accepted commitment bit) to A2
'''

def Agent2_recv():

    with CQCConnection("B2") as B2:
        sleep(wait)
        r = B2.recvClassical()
        print ("B2 ACCEPTS measurement list as r:")
        received2[:] = list(r)
        print ("B2 TRANSFORMES LIST:")
        sleep(wait)
        commitment = B2.recvClassical()[0]
        print ("received commitment by Agent2:", commitment)
        
        sleep(5)
        sleep(wait)
        B2.sendClassical("A2", received2)
        print ("received by B1:", received2)
        sleep(wait)
        B2.sendClassical("A2", commitment)
        print ("commitment by B1:", commitment)
        
        
if __name__ == "__main__":       
    Agent2_recv()        
