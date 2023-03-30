#!/bin/bash
NEWNAME=''
PID='ps aux | grep nginx'
echo $PID

nsenter --net=/proc/$PID/ns/net
ip netns add $NEWNAME
ip netns delete $NAME