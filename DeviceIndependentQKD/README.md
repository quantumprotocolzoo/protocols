# Device Independent Quantum Key Distribution
The code in this directory provides an implementation of the DIQKD protocol (excluding error correction and privacy amplification) as described in the [Quantum Protocol Zoo](https://wiki.veriqloud.fr/index.php?title=Device-Independent_Quantum_Key_Distribution), using Netsquid. The steps of 'Distribution and measurement' and 'Parameter estimation' are implemented. At the end of the protocol, both Alice and Bob agree upon a secure key or agree to abort.

# Requirements
- 2 Nodes capable of single-qubit measurements in upto 3 bases (2 for Alice, 3 for Bob)
- A source generating EPR pairs
- Quantum channels from the source to each node
- Authenticated public classical channel between Alice and Bob

# Changing protocol parameters
Protocol and simulation parameters are defined in utils.py and can be modified as desired
