from cqc.pythonLib import CQCConnection, qubit

#####################################################################################################
#In this example, we produce fresh coin/random number with using quantum logical gates. 
# While creating quantum random generator, steps of coin analogy was used.For this 
# 1) a new qubit was produced and this stpe similar to fishing coin 
# 2) applied hadamard gate, this step can be equal that tossing a  coin in air 
# 3)Finally measured qubit and this is like that we can learn now the coin's result like head or tail  


def main():

    # Initialize the connection
    with CQCConnection("Alice") as Alice:    # Here 1)we connect a node (ALice)
        q = qubit(Alice)                          # 2)produced a fresh qubit
        q.H()                                   # 3)applied Hadamard gate
        coin = q.measure()                        # 4)mesaured the qubit and the result printed
        to_print = "{}".format(coin)         
        print("| " + to_print + " |")
        return coin


if __name__ == '__main__':
    coin_list = []          # here we defined an empty list for saving our generated numbers/coins
    for i in range(10):   # for producing 10random numbers/coin  used for loop
        coin_list.append(main())     # generated coins/number added in the list
    print('Quantum Coin', coin_list)                     # printed on the secreen

##################################################################################################
