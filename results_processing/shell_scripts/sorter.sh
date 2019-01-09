#!/bin/bash
declare -a MODELS=( "bph1" "bph2" "bph3" );
declare -a DATASETS=( "LWP475" "LWP479" "LWP481" "LWP484" );

for MODEL_VERSION in ${MODELS[@]};
do
printf "Working on model %s\n" "${MODEL_VERSION}"
for D in ${DATASETS[@]};
do
printf "\tWorking on dataset %s\n" "${D}"
# INPUT_DIR="/home/buck06191/Dropbox/phd/hypothermia/ABC/nrmse_SA/${MODEL_VERSION}/${D}" 
OUTPUT_DIR="/home/buck06191/repos/Github/hypothermia-bayescmd/data/ABC/nrmse_SA/${MODEL_VERSION}/${D}" 
#mkdir -p ${OUTPUT_DIR}
#printf "\t Reading from %s\n" "${INPUT_DIR}"
printf "\t Writing to %s\n" "${OUTPUT_DIR}"
head -n 100001 "${OUTPUT_DIR}/sorted_all_parameters.csv" > "${OUTPUT_DIR}/reduced_sorted_parameters.csv"
# (head -n1 "${INPUT_DIR}/all_parameters.csv" && sort -n -t, -k17,17 <(tail -n+2 "${INPUT_DIR}/all_parameters.csv")) > "${OUTPUT_DIR}/sorted_all_parameters.csv"
done
done
