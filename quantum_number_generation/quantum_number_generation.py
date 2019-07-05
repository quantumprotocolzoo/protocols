from cqc.pythonLib import CQCConnection, qubit

#####################################################################################################
#In this example, we produce fresh coin/random number with using quantum logical gates. 
# While creating quantum random generator, steps of coin analogy was used.For this 
# 1) a new qubit was produced and this stpe similar to fishing coin 
# 2) applied hadamard gate, this step can be equal that tossing a  coin in air 
# 3)Finally measured qubit and this is like that we can learn now the coin's result like head or tail  


def qrng(location_string='Alice') :
    with CQCConnection(location_string) as location:
        q = qubit(location)
        q.H()
        number = q.measure()
        print('Outcome of the measurement at', location, ':', number) ;
        return number

def test():
    print('Returned List of Quantum Random Numbers', [ qrng() for i in range(10)] )

if __name__ == '__main__': test()

##################################################################################################
