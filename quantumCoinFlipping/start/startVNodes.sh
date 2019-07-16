
# start the nodes ['Alice', 'Bob', 'Charlie']

cd "$NETSIM"/run

python startNode.py Alice &
python startNode.py Bob &
python startNode.py Charlie &
