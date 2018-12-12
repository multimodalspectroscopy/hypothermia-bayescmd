#!/bin/bash

for MODEL in `echo */`; 
do 
    for DATA in `echo ${MODEL}*.sh`; 
    do qsub "./${DATA}"; 
    done; 
done
