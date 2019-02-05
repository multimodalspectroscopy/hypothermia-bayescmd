#!/bin/bash
workon bayescmd
declare -a MODELS=("bph1" "bph2" "bph4");
declare -a DATASETS=( "LWP475" "LWP479" "LWP481" "LWP484" );

for M in ${MODELS[@]};
do
printf "Working on model %s\n" "${M}"
    for D in ${DATASETS[@]};
    do
    printf "\r\tWorking on dataset %s\n" "${D}"
    ARCHIVES_DIR="/home/buck06191/Legion_Archives/bp_hypothermia/nrmse_SA/model_selection/${D}/sorted_all_${M}.csv"

    python csv_modifier.py ${ARCHIVES_DIR} ${M}
    done
done