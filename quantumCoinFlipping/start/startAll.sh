ps aux | grep python | grep Test | awk {'print $2'} | xargs kill -9
ps aux | grep python | grep setup | awk {'print $2'} | xargs kill -9
ps aux | grep python | grep start | awk {'print $2'} | xargs kill -9
ps aux | grep python | grep Coin | awk {'print $2'} | xargs kill -9

sh "$NETSIM/quantumCoinFlippingv2/start/startVNodes.sh"

sleep 5s

sh "$NETSIM/quantumCoinFlippingv2/start/startCQCNodes.sh"

