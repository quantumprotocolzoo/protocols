# pip install qiskit

import numpy as np

#import matplotlib.pyplot as plt
# from qiskit import *

# Global Variables describing message and authentication

n = 2
r = 2
s = int(n/r)
len_k = s
len_e = n+s

# ECC for (n + s = 3)

# Classical Error Correction Matrices

# C2 = Dual of hamming code (3->7)
# C2_perp = hamming code (4->7)

G_p = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1]]
H_p = [[0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1], [1, 0, 1, 0, 1, 0, 1]]
K = [[0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0]]

'''
# C2 = Dual of repetition code (2->3)
# C2_perp = repetition code (1->3)

G_p = [1, 1, 1]
H_p = [[1, 1, 0], [0, 1, 1]]
K = [[0, 1, 1], [0, 0, 1]]
'''



def GenKey():
  return np.random.randint(0, 2, len_k), np.random.randint(0, 2, len_e), np.random.randint(0, 2, len(G_p))

def ConvToInt(arr):
  res = int("".join(str(x) for x in arr), 2) 
  return res

k, e, b = GenKey()
print(k)
print(e)
print(b)



def Send():
  
  def GenMsg():
    return np.random.randint(0, 2, n)
  
  msg = GenMsg()
  print("Actual Message: ", msg)
  
  def MakeMi(message):
    m = []
    for i in range(0,n,s):
      m.append(ConvToInt(message[i:i+s]))
    return m

  def MakeMr():
    m = MakeMi(msg)
    f_k = 0

    for i in range(0,r):
      f_k += m[i]*(ConvToInt(k)**(r-i))

    f_k = f_k%(2**s)
    return (2**s - f_k)%(2**s)

  def MakeMsgToSend():
    msgToSend=msg
    Mr = bin(MakeMr())[2:].zfill(s)
    msgToSend = np.array(np.append(msgToSend, list(Mr)), dtype=int)
    XORed_msg = ConvToInt(msgToSend) ^ ConvToInt(e)
    y = list(bin(XORed_msg)[2:].zfill(len(e)))
    return (np.array(y, dtype=int))

  y = MakeMsgToSend()
  print("Message to be sent (without EC): ", y)
  
  z0 = np.mod(np.matmul(np.transpose(y), K), 2)
  random_choice = np.random.randint(0, 2, 4)
  z = np.mod(z0 + np.matmul(G_p, np.transpose(random_choice)), 2) 
  print("Message to be sent (with EC): ", z)
  
  return z

def Receive(received_msg):
  y_dec = np.mod(np.matmul(H_p, np.transpose(received_msg)), 2)
  print("Received message after EC: ", y_dec)

  XORed_msg_dec = ConvToInt(y_dec) ^ ConvToInt(e)
  Mis_dec = list(bin(XORed_msg_dec)[2:].zfill(len(e)))
  Mis_dec = np.array([int(x) for x in Mis_dec])
  print("Actual message received: ", Mis_dec[:-s])
  return Mis_dec[:-s]

def main():
  sent_message = Send()
  print("Send and Receive the message with bits to be sent in the X basis if the corresponding bit in b is 0, else in the Z basis.")
  received_message = Receive(sent_message) 

if __name__ == "__main__":
    main()



