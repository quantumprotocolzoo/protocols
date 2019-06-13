from cqc.pythonLib import CQCConnection, qubit

#####################################################################################################


def quantum_coin_generation(coin):

    # Initialize the connection
    with CQCConnection("Alice") as Alice:    # Here 1)we connect a node (ALice)
        q = qubit(Alice)                          # 2)produced a fresh qubit
        q.H()                                   # 3)applied Hadamard gate
        coin = q.measure()                        # 4)mesaured the qubit and the result printed
        to_print = "{}".format(coin)         
        print("| " + to_print + " |")
        return coin
     

coin_list = []          # here we defined an empty list for saving our generated numbers/coins
coin = 0
for i in range(10):   # for producing 10random numbers/coin  used for loop
    coin_list.append(quantum_coin_generation(coin))     # generated coins/number added in the list
print('Quantum Coin', coin_list)                     # printed on the secreen

##################################################################################################
