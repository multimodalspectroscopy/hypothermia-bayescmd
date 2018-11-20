#!/bin/bash

DATASET="LWP479"
OUTDIR=`readlink -m "../../data/SA_results/${DATASET}"`
JOBFILE=hypothermia_SA.dsimjob
DATAFILE="../../data/clean_hypothermia/${DATASET}_filtered_formatted.csv"
echo "Writing to ${OUTDIR}"
mkdir -p ${OUTDIR}
python ~/repos/Github/BayesCMD/batch/dsim.py -o ${OUTDIR} -b ~/repos/Github/BayesCMD/build ${JOBFILE} ${DATAFILE}

