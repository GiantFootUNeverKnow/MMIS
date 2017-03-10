# This script should be run under the experiment directory. For example Experiment/E9/
cd ../..
for i in {1..9}
do
    for j in {1..12}
    do
        echo algorithm $i runnning on job base $j
        time ./main.py --experiment Experiment/E14/config$i --jb Experiment/E14/E14.$j/jobs > Experiment/E14/E14.$j/result$i
    done
done
