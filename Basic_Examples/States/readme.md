For Bellstates code:

You can start simulaqron with default mode
Of course code can be divided 2 parts  such as Alice part and Bob part easily
And of course Alice can produce one qubit and it can send qubit to Bob. 
After Bob receiving the qubit it can produce an another qubit 
and the code can continue this type. THis is not a problem

For nPartyGHZStates code:

This code provide generating GHZ states according to number of inputs from users
1)If users give 2 names, code will stop because GHZ states need 3 party at least
2)After finishing names, first Alice start to creating EPR states except herself
3)According to numbers of inputs, other parties accept EPR states and produced a fresh qubit and then apply cnot gate
finally they measure their qubits
4)Again after contolling the number of inputs, parties send qubits to other parties (except themselves)

Please do not forgat to start simulaqron with names that you want to use



