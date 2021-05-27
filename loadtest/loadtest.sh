#!/bin/bash
mkdir -p results
for i in *.jmx; do
  echo "testing $i"
  jmeter -n -t $i -l results/results-$i
done
