#!/bin/bash

for i in {1..80}
do
  ip netns add ns$i
done

