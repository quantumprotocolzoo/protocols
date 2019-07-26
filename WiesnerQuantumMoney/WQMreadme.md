In this part, we implemented protocol of Wiesner Quantum Money
You can find the detailed knowledge from here: http://users.cms.caltech.edu/~vidick/teaching/120_qcrypto/wiesner.pdf


For the first part:
In the WQM1.py code:
suppose that: Alice is a bank and Bob is the user

1)Bank(Alice) prepares the banknotes from the BB84 states with a unique serial number
2)Bank(Alice) send the qubits to user(Bob)
Note that: In this code M = number of banknotes and N is the number of qubits for each banknotes

In the WQM2.py code:

1)Bob recv qubits 
2)Bob saves the qubits in a list with serial numbers

For the second part:
In the WQM2.py
1)Bob chooses the serial number between 0 and M(numberof banknotes)-1
2)Bob sends the serial number to the Bank(Alice)
3)Then Bob send the al qubits to the Bank with serial numbers to the Bank

In the WQM1.py
1)The bank first accepts the serial number
2)Then receive qubits and measures
(Before the measuring, bank applies the Hadamard gate according to value of basis)
3)If the result of measurement is not equal to the bits of banks then CHEATING!!
4)If the result of measurement is equal to the bits of banks then MONEY IS SECURE!






