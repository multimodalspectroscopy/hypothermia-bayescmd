#!/bin/bash

DATASET="LWP481"
OUTDIR1=`readlink -m "../../data/SA_results/bph_2/with_cellDeath/nrmse/${DATASET}"`
OUTDIR2=`readlink -m "../../data/SA_results/bph_2/with_cellDeath/nrmse_zero/${DATASET}"`
JOBFILE1=hypothermia_SA.dsimjob
JOBFILE2=hypothermia_SA_zero.dsimjob
DATAFILE="../../data/clean_hypothermia/${DATASET}_filtered_formatted.csv"

echo "Writing to ${OUTDIR1}"
mkdir -p ${OUTDIR1}
mkdir -p ${OUTDIR2}
python ~/repos/Github/BayesCMD/batch/dsim.py -o ${OUTDIR1} -b ~/repos/Github/BayesCMD/build ${JOBFILE1} ${DATAFILE}

echo "Writing to ${OUTDIR2}"
mkdir -p ${OUTDIR2}
mkdir -p ${OUTDIR2}
python ~/repos/Github/BayesCMD/batch/dsim.py -o ${OUTDIR2} -b ~/repos/Github/BayesCMD/build ${JOBFILE2} ${DATAFILE}