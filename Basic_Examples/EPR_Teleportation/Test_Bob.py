from cqc.pythonLib import CQCConnection, qubit
from teleportation import accept_teleportation

if __name__ == '__main__':
    with CQCConnection("Bob") as location:
        q = accept_teleportation(location)
        m = q.measure()
        print("m", m)
