# This script should be run under the experiment directory. For example Experiment/E13/
cd ../..
for i in {1..4}
do
    COUNT=0
    for j in 50 100 200 400
    do
        COUNT+=1
        echo algorithm $i is running on job base $j sequence $COUNT
        time ./main.py --experiment Experiment/E18/config$i --jb Experiment/E18/jobs_$j --repeat 10000 > Experiment/E18/result${j}_${i}       
    done
done

