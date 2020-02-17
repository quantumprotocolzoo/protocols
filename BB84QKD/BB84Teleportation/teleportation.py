from cqc.pythonLib import CQCConnection, qubit
from time import sleep

wait = 2
def send_teleportation(q,sender,receiver):
            qA = sender.createEPR(receiver)
            #q = qubit(location)
            q.cnot(qA)
            q.H()
            a = q.measure()
            b = qA.measure()
            # print('Corrections were sent at', location, ':', [a, b]) #
            # print("location,location_string, location2, location_string2", location,location_string,location2,location_string2)
            sender.sendClassical(receiver, [a, b])
            print('Corrections were sent at', sender, ':', [a, b]) #
            return [a,b]



def accept_teleportation(receiver):
        qB = receiver.recvEPR()
        message = list(receiver.recvClassical())
        print("data: ", message)
        if message[1] == 1:
            qB.X()
        if message[0] == 1:
            qB.Z() 


        return qB



# if __name__ == '__main__':
    
   # with CQCConnection("Alice") as location:
   #     q = qubit(location)
   #     send_teleportation(q,location,'Bob')
