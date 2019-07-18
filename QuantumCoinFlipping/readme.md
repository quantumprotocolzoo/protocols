For implementing Quantum Protocol Zoo's  Quantum Coin Flipping protocol, 
"Unconditionally Secure Quantum Coin Tossing" was used.

In the CoinFlippingAlice code:

In the first step:
1) Alice produces random bits which are called a_bits from j to m
2) Alice produces other random bits which are called c_bits for each a_bits   from i to n

In the second step:
1) Alice produces 2 qubits
2) After producing qubits, according to c_bits value applied rot_X 
Note: at this point 14 degree was used as angle in order to provide the paper's steps:
"Unconditionally Secure Quantum Coin Tossing"
3) Alice sends Bob qubits
4) By the way, after these steps, Alice accepts the qubits from Bob

In the third step:
1) Alice send Bob the xor a_bits^cbits as classical message
2) After sending xor bits, Alice accepts classical messages and qubits from Bob.
3) According to accepted classical message's value from Bob, Alice sends qubits to Bob


In the fourth and fifth steps:
1) Alice send Bob a_bits as classical message
2) Alie also accepts classical message from Bob
3) According to accepted message value, applied rot_X
4) And then qubits were measured

and the same thing was done for opposite a_bits. This time
1) According to opposite a_bits(which is called a_j_bar) applied rot_X
2) After applying rot_X, qubits were measured

In the final step:
The final bit of each of the party is the xor of xor of the random bits,
they prepared in the first step and xor of the bits they measured in the fourth step. 
This final bit is the random bit which has come up in the 'coin toss'. 
Thus ends the protocol.


In the CoinFlippingBob code:

In the first step:
1) Bob produces random bits which are called b_bits from j to m
2) Bob produces other random bits which are called d_bits for each b_bits   from i to n

In the second step:
1) Bob produces 2 qubits
2) After producing qubits, according to d_bits value applied rot_X 
Note: at this point 14 degree was used as angle in order to provide the paper's steps:
"Unconditionally Secure Quantum Coin Tossing"
3) Bob sends qubits to Alice
4) By the way, after these steps, Bob accepts the qubits from Alice

In the third step:
Note: In this part queue of process related to simulaqron-cqc architecture
1) Bob should accept the xor a_bits^cbits e_ij as classical message from Alice
2) Bob send Alice the xor b_bits^dbits as classical message f_ij
3) According to value of e_ij from Alice, Bob sends qubits to Alice
 
In the fourth and fifth steps:
1) Bob accepts a_bits as a classical message from Alice
2) Bob sends b-bits as a classical message to Alice
3) According to value of accepted a_bits. applied rotX 
4) And qubits were measured

the same process was done for opposite b_bits. This time
1) According to opposite b_bits (which is called b_j_bar) applied rot_X
2) After applying rot_X, qubits were measured

In the final step:
The final bit of each of the party is the xor of xor of the random bits,
they prepared in the first step and xor of the bits they measured in the fourth step. 
This final bit is the random bit which has come up in the 'coin toss'. 
Thus ends the protocol.

Results of these 2 final steps should be same
