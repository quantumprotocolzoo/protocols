In this example BB84 protocol was implemented with using CQC library (Simulaqron) and Pyhton

In the BB84Alice.py part:

1)Alice produces a secret key (100 bit)

2)For encoding the secret key ALice produce her basis (100 basis)

3)Then Alice creates a fresh qubit.

  3.1) If Alice's bits equal 1 --> Alice  applies X gate for her qubit
  
  3.2) If Alice's basis equal 1 --> Alice applies H gate for her qubit
  
  3.3) And ALice sends her qubit to Bob
  
  
4) Alice send her basis to Bob  

In the BB84Bob.py part:

1)Bob receive qubit from Alice

2)Bob produces his basis and he saves in the basis_bob list

 2.1)If Bob basis equal to 1-->Bob apply H gate for his qubit
 
3)Bob measures the qubit and saves in the received list

4)Bob receive classical message from Alice and he saves in the basis_alice list


(Note: Dont worry before the saving in basis_alice list used basis_alice[:] 
because basis_alice is a global variable)

In the calculation function:

1)If alice_basis and bob_basis equal saved the correct values 
and for testing save the correct index

 1.a)If it is not equal than this is an arror 

2)And some calculaton such as error percentage

