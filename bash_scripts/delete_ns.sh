#!/bin/bash
FILE='delete_ns.sh'
chmod +x $FILE
echo "deleting namespace"
NAME='testing'
sudo ip netns delete $NAME
