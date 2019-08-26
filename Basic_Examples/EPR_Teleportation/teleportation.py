from cqc.pythonLib import CQCConnection, qubit

def send_teleportation(q,sender,receiver):
    qA = sender.createEPR(receiver)
    q.cnot(qA)
    q.H()
    a = q.measure()
    b = qA.measure()
    sender.sendClassical(receiver, [a, b])
    print('Corrections were sent at', sender, ':', [a, b])
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
