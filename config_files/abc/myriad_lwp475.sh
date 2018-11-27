#!/bin/bash -l
#$ -l h_rt=1:30:00
#$ -N LWP475_cellDeath
#$ -wd /home/ucbpjru/Scratch
# Set up the job array.  In this instance we have requested 1000 tasks
# numbered 1 to 1000.
#$ -t 1

module load python3/recommended
cd $TMPDIR
export BASEDIR="$HOME/BayesCMD"

DATASET="LWP475"
DATADIR=`readink -m "../../data/clean_hypothermia/${DATASET}_filtered_formatted.csv"`
CONFIGFILE=`readlink -m "./bp_hypothermia_config.json"`


start=`date +%s`
python3 $BASEDIR/scripts/batch.py 1000 $DATAFILE $CONFIGFILE --workdir $TMPDIR
echo "Duration: $(($(date +%s)-$start))" > $TMPDIR/$SGE_TASK_ID.timings.txt

tar -zcvf $HOME/Scratch/batch_$JOB_NAME.$SGE_TASK_ID.tar.gz $TMPDIR
