#!/bin/bash

rm data/model.pickle
cat tmp/training.csv | python csirtg_ipsml/train.py --save data/model.pickle
