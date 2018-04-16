#!/bin/bash

rm -rf tmp
mkdir -p tmp

echo "creating whitelist"
cat data/whitelist.txt | python csirtg_ipsml/ip.py --good > tmp/whitelist.csv

echo "creating blacklist"
cat data/blacklist.txt | python csirtg_ipsml/ip.py > tmp/blacklist.csv

echo "merging lists"
cat tmp/whitelist.csv tmp/blacklist.csv | gshuf > tmp/training.csv

TESTS="128.205.1.1"

for T in $TESTS; do
  echo "Testing $T"
  cat tmp/training.csv | python csirtg_ipsml/train.py -i $T
done
