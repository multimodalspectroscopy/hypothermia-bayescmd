#!/bin/bash

DATASET="LWP479"
OUTDIR=`readlink -m "../../data/openopt_results/with_cellDeath/${DATASET}"`
JOBFILE="${DATASET}_hypothermia.optjob"
DATAFILE="../../data/clean_hypothermia/${DATASET}_filtered_formatted.csv"
echo "Writing to ${OUTDIR}" 
mkdir -p ${OUTDIR}
python -u ~/repos/Github/BayesCMD/batch/optim.py -o ${OUTDIR} -b ~/repos/Github/BayesCMD/build ${JOBFILE}  ${DATAFILE} | tee -a "${OUTDIR}/fitting_output.txt"



