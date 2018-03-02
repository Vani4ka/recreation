#!/bin/bash

python2.7 recreation-optimise.py

for i in `seq 20`;
do
    python2.7 recreation-optimise-stopping.py
done