# This script should be run under the experiment directory. For example Experiment/E9/
cd ../..
for i in {1..3}
do
    for j in {1..4}
    do
        echo algorithm $i runnning on job base $j
        time ./main.py --experiment Experiment/E17/config$i --jb Experiment/E17/E17.$j/jobs > Experiment/E17/E17.$j/result$i
    done
done
