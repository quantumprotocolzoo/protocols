from cqc.pythonLib import CQCConnection, qubit


'''
This code provide generating GHZ states according to number of inputs from users
1)If users give 2 names, code will stop because GHZ states need 3 party at least
2)After finishing names, first Alice start to creating EPR states except herself
3)According to numbers of inputs, other parties accept EPR states and produced a fresh qubit and then apply cnot gate
finally they measure their qubits
4)Again after contolling the number of inputs, parties send qubits to other parties (except themselves)
'''


arr = []  # Here an empty array was defined and users can give name. After finishing names, users should press enter
veri = input("Add person")   
while veri:                     
    arr.append(veri)
    veri = input("Add person")

if len(arr) == 2: 
    print("For Generating GHZ state party number should be 3 at least!!! Please try again") 
    raise SystemExit
   

def main():
    with CQCConnection("Alice") as Alice:
        for i in range (len(arr)):
            if 'Alice' != arr[i]:
                qEPR = Alice.createEPR(arr[i])
                m = qEPR.measure()
                to_print = "App {}:Part 1: Measurement outcome is: {}".format(arr[0], m)
                print("| " + to_print + " |")

    with CQCConnection("Bob") as Bob:
        qBEPR = Bob.recvEPR()
        print("OK 1")
        qnew = qubit(Bob)
        qBEPR.cnot(qnew)
        m = qBEPR.measure()
        to_print2 = "App {}: Part 2: Measurement outcome is: {}".format(arr[1], m)
        print("| " + to_print2 + " |")
            for i in range (len(arr)):
                if 'Alice' != arr[i] and 'Bob' != arr[i]:
                    qnew = qubit(Bob)
                    Bob.sendQubit(qnew,arr[i])
       
        
       
   
    with CQCConnection("Eve") as Eve: 
        if len(arr) >= 3:
            qEEPR = Eve.recvEPR()
            print("OK 2")
            qnew = Eve.recvQubit()
            qEEPR.cnot(qnew)
            m = qEEPR.measure()
            to_print3 = "App {}: Part 3: Measurement outcome is: {}".format(arr[2], m)
            print("| " + to_print3 + " |")
            for i in range (len(arr)):
                if 'Alice' != arr[i] and 'Bob' != arr[i] and 'Eve' != arr[i]:
                    qnew = qubit(Eve)
                    Eve.sendQubit(qnew,arr[i])
         
      
         
    with CQCConnection("David") as David:
        if len(arr) >= 4:
            qDEPR = David.recvEPR()
            print("OK 3")
            qnew = David.recvQubit()
            qDEPR.cnot(qnew)
            m = qDEPR.measure()
            to_print4 = "App {}: Part 4: Measurement outcome is: {}".format(arr[3], m)
            print("| " + to_print4 + " |")
            for i in range (len(arr)):
                if 'Alice' != arr[i] and 'Bob' != arr[i] and 'Eve' != arr[i] and 'David' != arr[i]: 
                    qnew = qubit(David)
                    David.sendQubit(qnew,arr[i])

    with CQCConnection("Charlie") as Charlie:
        if len(arr) >= 5:
            qCEPR = Charlie.recvEPR()
            print("OK 4")
            qnew = Charlie.recvQubit()
            qCEPR.cnot(qnew) 
            m = qCEPR.measure()
            to_print5 = "App {}: Part 5: Measurement outcome is: {}".format(arr[4], m)
            print("| " + to_print5 + " |")
           
         


if __name__ == "__main__":
 
 main()
