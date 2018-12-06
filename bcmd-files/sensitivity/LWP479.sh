#!/bin/bash
# Call each model in turn

for i in {1..3};
do
    /home/buck06191/repos/Github/hypothermia-bayescmd/bcmd-files/sensitivity/bp_hypothermia_${i}/SA_LWP479.sh "/home/buck06191/repos/Github/hypothermia-bayescmd/bcmd-files/sensitivity/bp_hypothermia_${i}/"
done