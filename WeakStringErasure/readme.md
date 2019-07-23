In this part, we implemented Weak String Erasure protocol. 
You can find the detailed knowledge from here: https://wiki.veriqloud.fr/index.php?title=Weak_String_Erasure

In the WSEAlice.py code:
1)First, Alice produces n bits and n basis randomly
2)Alice produces fresh qubits
3)According to values of bits and basis, applied X or H gate
4)Alice sends qubits to Bob
After these steps the second part begins for Alice
5)For security Alice and Bob wait for a specific time
6)After this Alice send her basis to Bob


In the WSEBob.py code:
1)First Bob receive qubits
2)Bob produces his basis randomly
3)According to values of Bob's basis, Bob applies H gate
After these steps the second part begins for Bob
4)For security Alice and Bob wait for a specific time
5)Bob receivebasis from Alice
6)if basis bob and received basis from alice are equal to each other, the ture values and indexes are saved in new lists
