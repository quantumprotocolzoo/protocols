==================================
Quantum Digital Signature Protocol
==================================

This project contains the SimulaQron implementation of the quantum digital signature protocol based on the following papers:
        
        "Quantum digital signatures with quantum key distribution components" - P. Wallden et al.
        https://arxiv.org/abs/1403.5551

        "Experimental demonstration of kilometer-range quantum digital signatures" - R. Donaldson et al.
        https://arxiv.org/abs/1509.07827


The protocol is a variant on the P1' protocol described in the first paper but with the variation that Bob (Charlie) will verify the signature by comparing Alice's declaration to the L/2 measurements he made directly and the L/2 measurements he received from Charlie (Bob) independently. If either one of these strings contains more than the pre-agreed threshold, that party will abort.

This file also contains an Estimate_Parameters file which allows suitable values of s_a and s_v to be generated. This is done counting how many mismatches are caused by a certain level of error and a certain level of channel loss. This is compared to the analytical values.

DESCRIPTION OF PROTOCOL
=======================

DISTRIBUTION STAGE:
    - Alice generates a classical string (b^k_l) where b^k_l is one of the 4 BB84 states for l=1,...,L for each possible message k. In this case, k is a single bit message. This will be her private key.
    - Alice generates qubit strings according to her private key, |b^0,1>...|b^1,L>, and sends copies to Bob and Charlie. The complete state of the qubits will only be known to Alice who holds the classical description of them.
    - Bob and Charlie immediately make measurements of the received qubits, randomly and independently selecting one of the BB84 bases to measure a quantum signature element (one of the |b^k_l>) in. This measurement rules out one of the states that Alice could have prepared the qubit in and so Bob and Charlie record this so called unambiguous state elimination (USE) measurement.

SYMMETRISATION STAGE
    - To prevent against repudiation, Bob and Charlie secretly select half of their measurements to send to the other. Thus they each end up with two strings of USE measurements of length L/2. Since this is done in secret, i.e. without Alice knowing who has which measurements, the system is now completely symmetric from Alice's point of view.

SIGNING STAGE
    - To sign the message m, Alice declares the message and the corresponding private key for that message to Bob, (m, b^m_1,...b^m_L).
    - Bob compares the classical description of the qubit string (the private key) to his two USE measurement strings. If in either one of the strings he counts more than saL/2 mismatches then he aborts, otherwise he accepts the message.

    TRANSFER STAGE
    - Bob transfers the message by declaring (m, b^m_1,...b^m_L) to Charlie who verifies the signature by the same method as Bob except using the threshold svL/s where sv>sa.

IMPLEMENTATION
==============

The implementation makes use of the develop branch of SimulaQron. The current proBeta branch does not work with the implementation and will return a "cannot connect to server error" when two parties try to send a classical message to the same node.

The project contains three versions: all parties are honest, Alice attempts to repudiate, Bob attempts to forge. To run a particular version, open the desired folder in command line and run the stages one by one (waiting for each to finish) with:

                            sh doNewDistribution.sh
                            sh doNewSymmetrisation.sh
                            sh doNewSigning.sh
                            sh doNewTransfer.sh

The project also contains a config file which defines the parameters of each run. The file has the following format:

    (L - signature length [integer])
    (N - size of message [integer])
    (sa - Bob's threshold [float])
    (sv - Charlie's threshold [float])
    (Level of noise in the quantum channel [float])


It should be noted that the code for ACKSend and ACKRecv were borrowed from the QChat project by Matthew Skrzypczyk (http://www.simulaqron.org/competition/).






