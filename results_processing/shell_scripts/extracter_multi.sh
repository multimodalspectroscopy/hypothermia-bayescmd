#!/bin/bash
declare -a MODELS=( "bph1" "bph2" "bph4" );
declare -a DATASETS=( "LWP475" "LWP479" "LWP481" "LWP484" );

for MODEL_VERSION in ${MODELS[@]};
do
printf "Working on model %s\n" "${MODEL_VERSION}"
for D in ${DATASETS[@]};
do
printf "Working on dataset %s\n" "${D}"
    for i in {1..50005};
    do
    printf "\tWorking on batch %6d\n" "${i}"
    OUTPUT_DIR="/home/buck06191/Dropbox/phd/hypothermia/ABC/nrmse_SA/${MODEL_VERSION}/${D}/params_$i"
    ARCHIVES_DIR="/home/buck06191/Legion_Archives/bp_hypothermia/final_selection/${MODEL_VERSION}/${D}/batch_${D}_cellDeath_${MODEL_VERSION:3:1}.$i.tar.gz"
    mkdir -p $OUTPUT_DIR
    tar -xzf $ARCHIVES_DIR -C $OUTPUT_DIR --wildcards --no-anchored --strip-components 3 '*/*/*/parameters.csv'
    done
done
done
