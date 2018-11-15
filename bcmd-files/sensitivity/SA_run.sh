#!/bin/bash

DATASET="LWP484"
OUTDIR="../../data/SA_results/${DATASET}"
mkdir -p ${OUTDIR}
python ~/repos/Github/BayesCMD/batch/dsim.py -o ${OUTDIR} hypothermia_SA.dsimjob -b ~/repos/Github/BayesCMD/build ../../data/clean_hypothermia/cleaned_${DATASET}_filtered.csv 
