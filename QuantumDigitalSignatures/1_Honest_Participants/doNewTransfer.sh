ps aux | grep python | grep Test | awk {'print $2'} | xargs kill -9
ps aux | grep python | grep QDS | awk {'print $2'} | xargs kill -9


sh "$NETSIM/quantumDigitalSignatures/1_Honest_Participants/runTransfer.sh"

