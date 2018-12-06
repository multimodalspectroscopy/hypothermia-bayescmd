#!/bin/bash

DATASET="LWP475"
for i in {1..50000};
do
echo "Working on batch ${i}"
OUTPUT_DIR="/home/buck06191/Dropbox/phd/hypothermia/ABC/lwp475/params_$i"
ARCHIVES_DIR="/home/buck06191/Legion_Archives/batch_${DATASET}_cellDeath.$i.tar.gz"
mkdir -p $OUTPUT_DIR
tar -xzf $ARCHIVES_DIR -C $OUTPUT_DIR --wildcards --no-anchored --strip-components 3 '*/*/*/parameters.csv'
done
