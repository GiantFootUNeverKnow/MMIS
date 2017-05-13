# This script should be run under the experiment directory. For example Experiment/E13/
cd ../..

for i in {1..3}
do
    for j in {0..2}
    do
        echo algorithm $i is running on job base $j sequence
        time ./main.py --experiment Experiment/E21/config$i --jb Experiment/E21/jobs_$j > Experiment/E21/result${j}_${i}       
    done
done
for i in {4..6}
do
    for j in {0..2}
    do
        echo algorithm $i is running on job base $j sequence
        time ./main.py --experiment Experiment/E21/config$i --jb Experiment/E21/jobs_$j --repeat 10000 > Experiment/E21/result${j}_${i}       
    done
done
