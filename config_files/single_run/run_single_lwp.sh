DATASET="LWP479"
DATAFILE="/home/buck06191/repos/Github/hypothermia-bayescmd/data/clean_hypothermia/${DATASET}_filtered_formatted.csv"
CONFIG="/home/buck06191/repos/Github/hypothermia-bayescmd/config_files/single_run/${DATASET}_openopt.json"

echo ${DATAFILE}
echo ${CONFIG}
python "/home/buck06191/repos/Github/BayesCMD/scripts/single_run/run_model.py" --debug --workdir "/home/buck06191/repos/Github/hypothermia-bayescmd/data/openopt_results/${dataset}/fitting_run" ${DATAFILE} ${CONFIG}
