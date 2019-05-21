from cqc.pythonLib_protocols.coinflip_leader import CoinflipConsensus


def main():

    leaderChooser = CoinflipConsensus(arr)  # Elects a leader from array that you declared
    return leaderChooser.leader()

# For 12-13-14-15 lines: After seeing "Add person" sentence, you can add person that how many person you want to add.
#  After adding one person you should press "enter" and then you can continue to add person with press enter 
#  If you want to cancel from adding person you should press enter again
# After enter the all name that you wanted to add you should press "enter"
# Note that: you should use name from cqc's names space such as Alice, Bob, David, Eve Charlie.., you cant't use name randomly such as Gozde, Axel ...
arr = []  # Here an empty array was defined
veri = input("Add person")   
while veri:                     
    arr.append(veri)
    veri = input("Add person")
        

# giving a value for each leader
d = dict()
for veri in arr:
    d[veri] = 0
    
# Runs 20 rounds of leader election and prints the results.
for i in range(0, 20):
    if i % 10 == 0:
        print(i)
    d[main()] += 1


print(d)
