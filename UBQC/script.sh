#open two terminal, run script.sh in one and output bob to the other one (run tty to know /dev/pts/$i) 
#!/bin/bash

#Example 1 : execute CNOT gate on |+0> using MBQC. Expect [0,0] or [1,1] as measurement each time
# for i in `seq 25`
# do
#     python serverMBQC.py  >/dev/pts/2 &
#     python clientMBQC.py -c circuits/circuitCNOT.json -i H,I  
# done


#Example 2 : execute SWAP gate on |+-> using UBQC amd measure in the X basis. Expect [1,0] as measurement each time
for i in `seq 10`
do
#    python serverUBQC.py  >/dev/pts/0 &
	python serverUBQC.py &
    python clientUBQC.py -c circuits/circuitSWAP.json -i I,Z -o H,H  
done