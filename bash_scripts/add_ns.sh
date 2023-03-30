#!/bin/bash
FILE='add_ns.sh'
chmod +x $FILE
echo "adding namespace"
NAME='testing'
ip netns add $NAME