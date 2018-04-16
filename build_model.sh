#!/bin/bash

PYVER=`python -c 'import sys; print(".".join(map(str, sys.version_info[:1])))'`
MODEL=model.pickle
if [ ${PYVER} == "2" ]; then
  MODEL=model_py2.pickle
fi


rm data/${MODEL}
cat tmp/training.csv | python csirtg_ipsml/train.py --save data/${MODEL}

