from cqc.pythonLib import CQCConnection, qubit
from random import randint
#####################################################################################################

def quantum_coin_generation(coin):

    # Initialize the connection
    with CQCConnection("Alice") as Alice:
     q=qubit(Alice)
     q.H()
     coin=q.measure()
     #fresh_coin=int(coin)
     to_print = "{}".format(coin)
     print("| " + to_print + " |")
     return coin
     

coin_list=[]
coin=0
for i in range(10):
 coin_list.append(quantum_coin_generation(coin))
print('Quantum Coin', coin_list)

##################################################################################################
