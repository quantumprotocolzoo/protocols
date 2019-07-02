from cqc.pythonLib import CQCConnection, qubit
import argparse

'''
  This function(generate_bell_pair) for creating a bell pair from two qubit. 
  For this 1) created  qubit from Alice for will create message state
  2)created qubit from Bob for recreating the message state 
  3)applied Hadamard gate for qubit1
  4)appled cnot gate
'''


def generate_bell_pair():
    with CQCConnection("Alice") as Alice:
        qubit1 = qubit(Alice)
        with CQCConnection("Bob") as Bob:
            qubit2 = qubit(Alice)
            qubit1.H()
            qubit1.cnot(qubit2)
    return qubit1, qubit2
  

'''
In this furnction one of the entangled qubit was used as an input.
And a message value  is a bit (value 0 or 1) was used as an input.
1)A new fresh qubit was produced
2)If message value is equal 1, then qubit is set to positive
by flipping the base state with X gate
3)original qubit and message bit was entangled
4)Message qubit was put in superpositon
5)they were measured
6)Finally the qubits turn into normal bits
'''


def create_message(qubit1, message = 0):
    with CQCConnection("Alice") as Alice:
        qubit_send = qubit(Alice)
        qubit1 = qubit(Alice)
        if message == 1:
            qubit_send.X()
        qubit_send.cnot(qubit1)
        qubit_send.H()
        a = qubit_send.measure()
        b = qubit1.measure()
        classical_encoded_message  = [int(a), int(b)]
  #classical_encoded_message = "{}".format(a, b)
  # print ("classical_encoded_message", classical_encoded_message)
    return classical_encoded_message


'''
With This function, message is accepted and transformed classical 
encoded message. Second qubit from bell pair was used.
1)According to the 2 message value applied X or Z gate
2)qubits was measured
3)converted to int
'''


def message_reciever(message, qubit2):
     with CQCConnection("Bob") as Bob:
         qubit2 = qubit(Bob)
         if message[1] == 1:
             qubit2.X()
         if message[0] == 1:
             qubit2.Z()
         d = qubit2.measure()
         recieve_bit = d
         recieve_bit = int(d)
  # classical_encoded_message = create_message(qubit1 = qubit2, message = bit)
  # print ('recieve_bit',recieve_bit )
     return recieve_bit


'''
In this function
1) created bell pair
2)created message
3)After sending message reciever, results are returned
'''


def send_recieve(bit = 0):
    with CQCConnection("Alice") as Alice:
        with CQCConnection("Bob") as Bob:
            qubit2 = qubit(Bob)
            qubit1 = qubit(Alice)
            qubit1, qubit2 = generate_bell_pair()
            classical_encoded_message = create_message(qubit1 = qubit1, message = bit)
   # print ('classical_encoded_message',classical_encoded_message )
    return message_reciever(classical_encoded_message, qubit2)

  
'''
This is the last function of sending  message with 
using Quantum State Teleportation in CQC
1)When user run the code with a message, firstly message 
transformed binary encoded message
2)binary message is divided into a list 
3)iterated through each word and each bit
4)And thanks to send_recieve funtionbacking tho original letter
'''


def send_all_message(message = 'hello'):
    binary_encoded_message = [bin(ord(x))[2:].zfill(8) for x in message]
    print('Message to send: ', message)
    print('Binary message to send: ', binary_encoded_message)
    received_bytes_list = []
    for letter in binary_encoded_message:
        received_bits = ''
        for bit in letter:
            received_bits = received_bits + str(send_recieve(int(bit)))
  # print('received_bits22', received_bits)
        received_bytes_list.append(received_bits)
    binary_to_string = ''.join([chr(int(x, 2)) for x in received_bytes_list])
    print('Received Binary message: ', received_bytes_list)
    print('Received message: ', binary_to_string)

    
'''
Now user can run the code with like this sentence 
python3 quantum_state_teleportation.py -m deneme
NOte that I prefered the one words a message 
I have not tried the code more than one words.
Bests!!
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send a message using Quantum State Teleportation with CQC')
    requiredNamed = parser.add_argument_group('Required arguments')
    requiredNamed.add_argument('-m','--message',required=True, help='message')
    args = parser.parse_args()
    send_all_message(args.message)
