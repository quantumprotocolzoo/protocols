from cqc.pythonLib import CQCConnection, qubit
from time import sleep
received1 = []
wait = 1

'''
B1 accepts measurement list and commitment bit
And sleep(5) is a time space for second phase
After space time B1 sends to all knowledge(accepted commitment 
bit and accepted measurement list) to A1
'''

def Agent1_recv():

    with CQCConnection("B1") as B1:
        sleep(wait)
        r = B1.recvClassical()
        print ("B1 ACCEPTS measurement list from B0:")
        received1[:] = list(r)
        print ("B1 TRANSFORMES LIST")
        sleep(wait)
        commitment = B1.recvClassical()[0]
        print ("received commitment from B0:", commitment)
       
        sleep(5)
        sleep(wait)
        B1.sendClassical("A1", received1)
        print ("received by A1:", received1)
        sleep(wait)
        B1.sendClassical("A1",commitment)
        print ("commitment by A1:", commitment)
       
if __name__ == "__main__":       
    Agent1_recv()
