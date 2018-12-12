#!/bin/bash -l
#$ -l h_rt=1:30:00
#$ -N LWP479_cellDeath_1
#$ -o /home/ucbpjru/Scratch/bph1/LWP479/out
#$ -e /home/ucbpjru/Scratch/bph1/LWP479/err
#$ -wd /home/ucbpjru/Scratch
# Set up the job array.  In this instance we have requested 1000 tasks
# numbered 1 to 1000.
#$ -t 1-50000

module load python3/recommended
cd $TMPDIR
export BASEDIR="${HOME}/BayesCMD"

DATASET="LWP479"
DATAFILE="${HOME}/hypothermia-bayescmd/data/clean_hypothermia/${DATASET}_filtered_formatted.csv"
CONFIGFILE="${HOME}/hypothermia-bayescmd/config_files/abc/bp_hypothermnia_1/bp_hypothermia_1_config.json"

echo -e "Datafile is ${DATAFILE}\nConfig file is ${CONFIGFILE}."

start=`date +%s`
python3 $BASEDIR/scripts/batch.py 1000 $DATAFILE $CONFIGFILE --workdir $TMPDIR
echo "Duration: $(($(date +%s)-$start))" > $TMPDIR/$SGE_TASK_ID.timings.txt

tar -zcvf $HOME/Scratch/bph1/${DATASET}/batch_$JOB_NAME.$SGE_TASK_ID.tar.gz $TMPDIR
