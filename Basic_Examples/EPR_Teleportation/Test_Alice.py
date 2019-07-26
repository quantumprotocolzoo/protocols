from cqc.pythonLib import CQCConnection, qubit
from teleportation import send_teleportation

with CQCConnection("Alice") as location:
    q = qubit(location)
    send_teleportation(q,location,'Bob')
