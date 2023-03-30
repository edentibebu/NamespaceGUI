#!/bin/bash
echo "listing capabilities"
FILE='list_capabilities.sh'
chmod +x $FILE
NAME='testing' 
sudo ip netns exec $NAME capsh --print