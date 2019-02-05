#!/bin/bash

for MODEL in [1, 2, 4]; 
do 
    for DATA in `echo "./bp_hypothermia_${MODEL}/"*.sh`; 
    do qsub "./${DATA}"; 
    done; 
done
