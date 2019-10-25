In this exapmle, implemented QUantum Token protocol. You can find the detailed knowledge from here: 
"Experimental investigation of practical unforgeable quantum money" https://www.nature.com/articles/s41534-018-0058-2

Quantum Token code has 3 players: Bank is Alice, Client is Eve and Merchant is Bob

In the QuantumTokenBank.py code:

1) Bank(Alice) prepare the money. For this:

  -Bank prepares randombits and randombits2 and saves in a different list
  
  -Bank prepares randombasis for encoding the bits and saves in a list
  
  -Bank produces 2 qubits as qubit1 and qubit2
  
  -Bank applies gates according to the values of bits and basis
  
  -Bank saves these 2 qubits in a list which is called token 
  
2) Finally bank sends qubits to client
  
In the QuantumTokenClient.py code:

1) Client(Eve) receives qubits and then sends Merchant qubits.

After giving money to Merchant second stage is starting

In the QuantumTokenMerchant.py code:

1) Merchant(Bob) accepts qubits from Client

2) Merchant produces a bit randomly

3) According to the value of random bit, Merchant apply quantum gates

4) After applying gates, Merchant measures the qubits

5) After measuring qubits, the result of measurement and random bit are sent to Bank

In the QuantumTokenBank.py code:

1) Bank accepts qubits and bit from Merchant

2) After that Bank should check the values for preventing cheating. For this:

   -Bank looks value of accepted bit from Merchant and if it is equal to zero, then:
   
       -Bank looks value of its basis values
   
       -If these two values equal zero then:
   
           -Bank checks values of accepted bit and basis
       
               -If these two values different then:
           
                   -Cheating!!
      -If these value of basis is not equal zero then: 
          
          -cheating !!
          
   -If value of accepted bit is not equal to zero then:
   
       -If value of accepted bit and basis are different from each other, then:
       
           -If that bank basis is equal zero
           
               -If value of accepted bit and bank basis are different, then:
               
                   -Cheating
                   
           -If bank basis is not equal zero, then:
            
               !Cheating
                
                
