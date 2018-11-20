#!/bin/bash

DATASET="LWP475"
OUTDIR=`readlink -m "../../data/openopt_results/${DATASET}"`
JOBFILE=`${DATASET}_hypothermia.optjob`
DATAFILE=`../../data/clean_hypothermia/${DATASET}_filtered_formatted.csv `
echo "Writing to ${OUTDIR}"
mkdir -p ${OUTDIR}
python ~/repos/Github/BayesCMD/batch/opt.py -o ${OUTDIR} -b ~/repos/Github/BayesCMD/build ${JOBFILE}  ${DATAFILE} 



