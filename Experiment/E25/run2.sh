# This script should be run under the experiment directory. For example Experiment/E9/
cd ../..
for i in {1..1}
do
    for j in {1..24}
    do
        echo algorithm $i runnning on job base $j
        time ./main.py --experiment Experiment/E25/config$i --jb Experiment/E25/E25.$j/jobs --repeat 100 > Experiment/E25/E25.$j/result$i
    done
done
