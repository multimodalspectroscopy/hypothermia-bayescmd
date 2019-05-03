#!/bin/bash
# Call each model in turn

workon bcmd;
declare -a DATASETS=( 'LWP475' 'LWP479' 'LWP481' 'LWP484' );

for D in ${DATASETS[@]};
do
    /home/buck06191/repos/Github/hypothermia-bayescmd/bcmd-files/sensitivity/bp_hypothermia_0/SA_${D}.sh "/home/buck06191/repos/Github/hypothermia-bayescmd/bcmd-files/sensitivity/bp_hypothermia_0/"
done