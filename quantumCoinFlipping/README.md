==================================
Quantum Coin Flipping Protocol
==================================

This project contains the SimulaQron implementation of the quantum coin flipping protocol based on the following papers:
        
        "Practical Quantum Coin Flipping" - A. Pappa et al.
        https://arxiv.org/abs/1106.1099

        "Experimental plug&play quantum coin flipping" - A. Pappa et al.
        https://www.nature.com/articles/ncomms4717


The protocol is an implementation of the basic coin flipping protocol described in the papers above. In the implementation, Alice's source was assummed to be a single photon source which meant that Bob always received at most one qubit from a pulse.

DESCRIPTION OF PROTOCOL
=======================

    - Alice chooses K pairs (alpha_i, c_i) where i=1,...,K. Alpha_i will correspond to the basis the ith pulse will be prepared in and c_i will correspond to the state of that pulse (see notes).
    - Alice sends the states to Bob who picks a random basis beta_i to measure each pulse in. Due to the lossy nature of the quantum channel, his first successful measurement may not be of the first photon.
    - If he makes at least one successful measurement from the K pulses, he sends to Alice the position of the first successful measurement, j, and a random bit b.
    - Alice replies to Bob with the basis and the state of that qubit, (alpha_j, c_j).
    - If alpha_j=beta_j and Bob's outcome is the same as the one Alice declares, or if alpha_j =/= beta_j, both parties agree that the coin value is c_j XOR b. If they did measure in the same basis but Alice's declared c_j is different from Bob's measurement, Bob aborts.

IMPLEMENTATION
==============

The implementation makes use of the Develop branch of SimulaQron although should in theory run in the ProBeta version.

The code makes use of arbitrary rotations, thus it is necessary to use a simulation backend that has this capability, such as projectq. You can then start simulaqron using the following commands:
    simulaqron reset
    simulaqron set backend projectq
    simulaqron start

The project contains four versions: all parties are honest, Alice attempts to cheat, Bob attempts to cheat, ideal coin flipping. These can be run going into the desired folder in command line and running 
    
        sh run.sh

The simulation files also contain a config file which defines the parameters of each run. The file has the following format:

    (K - number of pulses [integer])
    (y - security parameter [float])
    (F - channel loss [float])
    (qber - qubit error rate [float])

It should be noted that the code for ACKSend and ACKRecv were borrowed from the QChat project by Matthew Skrzypczyk (http://www.simulaqron.org/competition/).






