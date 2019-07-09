Code for Quantum Bit Commitment Protocol has 6 players which are named A0, B0, A1, B1, A2, B2.
Suppose that A1 and A2 are agents of A0 and B1 and B2 are agents of B0

In the A0.py code: 

 1)For producing n qubits from BB84 states and sending to B0, random bits and random basis were produced
 
 2)After sending the qubits to B0, all random bits and random basis were sent to A1 and A2(A1 and A2 can be thought A0's agents)
 
In the B0.py code:

 1)Bit for commitment was produced
 
 2)If commitment bit is equal to 1, B0 accepts qubit after applying H gate and then measured the qubit.
   If commitment bit is not equal to 1, then B0 just measures 
   
 3)After these steps, B0 sends all knowledge(outcomes of measurements and the commitment bit) to its all agents (B1 and B2)
 
In the B1.py code:

 1)B1 accepts all classical messages and sends the all accepted classical messages to A1
 
In the B2.py code:

 1)B2 accepts all classical messages and sends the all accepted classical messages to A2 
  
In the A1.py code:

 1)A1 accepts all messages which were sent to it
   
   1.1)Check that: if the receieved commitment bit is equal to received basis
     
     1.2)Check that: if the classic bits and received bits is equal-->If it yes, then ok
     1.2.1) If it is not, then Eve is here
     
 2) And finally A1 sends the received knowledge to A2
 
In the A2.py code:
  
  1)A2 receives all messages which were sent to it
  
  2)Check that: received knowledge from A1 and receieved knowledge from B2 is equal or not
   
   2.1)If it is OK, then commitment is OK:)
   2.2)If it is not OK, then something is wrong :(
   
In this protocol cheating was not used. Because of this reason, if you want to be sure that the code is correct, then you should'nt see that: "Bob is cheating"
Note that: This readme file for just an outline. For detailed knowledges were added in the code.
        
