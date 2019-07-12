from cqc.pythonLib import CQCConnection, qubit

def generate_bell_pair():

    with CQCConnection("Alice") as Alice:
        qubit1 = qubit(Alice)
        qubit2 = qubit(Alice)
        qubit1.H()
        qubit1.cnot(qubit2)
        n = qubit1.measure()
        Alice.sendQubit(qubit2, "Bob")
        to_print = "App {}:Part 1: Measurement outcome is: {}".format(Alice.name, n)
        print("| " + to_print + " |")
  
    with CQCConnection("Bob") as Bob:
        qubit3 = Bob.recvQubit()
        m = qubit3.measure()
        to_print = "App {}:Part 1: Measurement outcome is: {}".format(Bob.name, m)
        print("| " + to_print + " |")
 
 
if __name__ == "__main__":
 
    generate_bell_pair()
