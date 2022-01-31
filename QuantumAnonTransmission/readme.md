# Quantum Anonymous Transmission
The code in this directory provides an implementation of GHZ-based Quantum Anonymous Transmission as described in the [Quantum Protocol Zoo](https://wiki.veriqloud.fr/index.php?title=GHZ-based_Quantum_Anonymous_Transmission), using Netsquid. The protocol anonymously transmits a qubit from the sender to the receiver.

# Requirements
- All nodes in the network should be able to perform single-qubit gates, the CNOT gate, and single-qubit measurements
- A trusted GHZ-state source
- Quantum channels from the source to each node
- Each node should be able to broadcast classical messages to the other nodes in the network

# Running
- Requirement: Installation of the [NetSquid package](https://netsquid.org/)
- Running: The code can be run by executing anon_trans.py
    ```
    python3 anon_trans.py
    ```
    
    - By executing the above command, the code runs with the following default parameters
        -  Number of nodes in the network: 5
        -  Id of sender node: 0
        -  Id of receiver node: 4
        -  Message state to be transmitted: $$\frac{1}{\sqrt{2}}(\left|0\right\rangle + i\left|1\right\rangle)$$
    - The user can specify the 4 parameters by providing them as command line arguments. For example, 
      ```
      python3 anon_trans.py 5 0 4 0.707 0.707j
      ```
      runs the code with the default parameters. The arguments in order are as follows:
        - Number of nodes (more than 2) or ```num_nodes```
        - Id of sender (should range from 0 to ```num_nodes-1```)
        - Id of receiver (should range from 0 to ```num_nodes-1```)
        - ![\alpha](https://latex.codecogs.com/svg.latex?%5Calpha) (Complex number)
        - ![\beta](https://latex.codecogs.com/svg.latex?%5Cbeta) (Complex number),
        
        where the message state to be transmitted is  ![\alpha\left|0\right\rangle + \beta\left|1\right\rangle](https://latex.codecogs.com/svg.latex?%5Calpha%7C0%5Crangle+%5Cbeta%7C1%5Crangle). The input message state need not be normalized, as normalization is performed by the code. For example, the above command would be equivalent to:
        ```
        python3 anon_trans.py 5 0 4 1 1j
        ```
- Expected output: 
    - Simulation parameters
    - Confirmation of state reception