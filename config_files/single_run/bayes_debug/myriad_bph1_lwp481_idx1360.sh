#!/bin/bash -l
#$ -l h_rt=1:00:00
#$ -N LWP481_bph1_debug
#$ -wd /home/ucbpjru/Scratch
# Set up the job array.  In this instance we have requested 1000 tasks
# numbered 1 to 1000.

module load python3/recommended
cd $TMPDIR
export BASEDIR="${HOME}/BayesCMD"
mkdir -p $HOME/Scratch/debug/

DATASET="LWP481"
DATAFILE="${HOME}/hypothermia-bayescmd/data/clean_hypothermia/${DATASET}_filtered_formatted.csv"
CONFIGFILE="${HOME}/hypothermia-bayescmd/config_files/single_run/bayes_debug/bph1_lwp481_idx1360.json"

echo "Datafile is ${DATAFILE}\nConfig file is ${CONFIGFILE}."

python "${HOME}/BayesCMD/scripts/single_run/run_model.py" --workdir $TMPDIR ${DATAFILE} ${CONFIGFILE}

tar -zcvf $HOME/Scratch/debug/$JOB_NAME.tar.gz $TMPDIR