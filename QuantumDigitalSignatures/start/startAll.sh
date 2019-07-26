ps aux | grep python | grep Test | awk {'print $2'} | xargs kill -9
ps aux | grep python | grep setup | awk {'print $2'} | xargs kill -9
ps aux | grep python | grep start | awk {'print $2'} | xargs kill -9
ps aux | grep python | grep QDS | awk {'print $2'} | xargs kill -9

sh "$NETSIM/QDS/start/startVNodes.sh"

sleep 5s

sh "$NETSIM/QDS/start/startCQCNodes.sh"

