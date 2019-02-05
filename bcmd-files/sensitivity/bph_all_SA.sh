#!/bin/bash
# Call each model in turn

workon bcmd;
declare -a MODELS=("1" "2" "4")
declare -a DATASETS=( 'LWP475' 'LWP479' 'LWP481' 'LWP484' );
for M in ${MODELS[@]};
do
for D in ${DATASETS[@]};
do
    /home/buck06191/repos/Github/hypothermia-bayescmd/bcmd-files/sensitivity/bp_hypothermia_${M}/SA_${D}.sh "/home/buck06191/repos/Github/hypothermia-bayescmd/bcmd-files/sensitivity/bp_hypothermia_${M}/"
done
done