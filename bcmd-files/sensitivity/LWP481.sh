#!/bin/bash
# Call each model in turn

for i in 3;
do
    /home/buck06191/repos/Github/hypothermia-bayescmd/bcmd-files/sensitivity/bp_hypothermia_${i}/SA_LWP481.sh "/home/buck06191/repos/Github/hypothermia-bayescmd/bcmd-files/sensitivity/bp_hypothermia_${i}/"
done