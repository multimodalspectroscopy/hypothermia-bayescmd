#!/bin/bash
declare -a MODELS=( "bph4" );
declare -a DATASETS=( "LWP475" "LWP479" "LWP481" "LWP484" );

for MODEL_VERSION in ${MODELS[@]};
do
printf "Working on model %s\n" "${MODEL_VERSION}"
for D in ${DATASETS[@]};
do
printf "\tWorking on dataset %s\n" "${D}"
INPUT_DIR="/home/buck06191/Dropbox/phd/hypothermia/ABC/nrmse_SA/${MODEL_VERSION}/${D}" 
# OUTPUT_DIR="/home/buck06191/repos/Github/hypothermia-bayescmd/data/ABC/nrmse_SA/${MODEL_VERSION}/${D}" 
#mkdir -p ${OUTPUT_DIR}
printf "\t Reading from %s\n" "${INPUT_DIR}"
printf "\t Writing to %s\n" "${INPUT_DIR}"
(head -n1 "${INPUT_DIR}/all_parameters.csv" && sort -n -t, -k17,17 <(tail -n+2 "${INPUT_DIR}/all_parameters.csv")) > "${INPUT_DIR}/sorted_all_parameters.csv"
head -n 100001 "${INPUT_DIR}/sorted_all_parameters.csv" > "${INPUT_DIR}/reduced_sorted_parameters.csv"
# (head -n1 "${INPUT_DIR}/all_parameters.csv" && sort -n -t, -k17,17 <(tail -n+2 "${INPUT_DIR}/all_parameters.csv")) > "${OUTPUT_DIR}/sorted_all_parameters.csv"
done
done
