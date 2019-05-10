#!/bin/bash
DATASET="LWP481"
DATAFILE="/home/buck06191/repos/Github/hypothermia-bayescmd/data/clean_hypothermia/${DATASET}_filtered_formatted.csv"
CONFIG="/home/buck06191/repos/Github/hypothermia-bayescmd/config_files/single_run/bayes_debug/bph1_lwp481_idx1360.json"

echo ${DATAFILE}
echo ${CONFIG}
python "/home/buck06191/repos/Github/BayesCMD/scripts/single_run/run_model.py" --workdir "/home/buck06191/repos/Github/hypothermia-bayescmd/data/ABC/debugging" ${DATAFILE} ${CONFIG}
