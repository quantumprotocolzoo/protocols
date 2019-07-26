
# start the nodes ['Alice', 'Bob', 'Charlie']

cd "$NETSIM"/run

python startCQC.py Alice &
python startCQC.py Bob &
python startCQC.py Charlie &
