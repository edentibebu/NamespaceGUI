#!/bin/bash

for i in {0..180}
do
    ip netns delete ns$i
done
