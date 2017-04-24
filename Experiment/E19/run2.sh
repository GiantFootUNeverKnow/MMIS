# This script should be run under the experiment directory. For example Experiment/E9/
cd ../..
for i in {1..12}
do
    for j in {1..12}
    do
        echo algorithm $i runnning on job base $j
        time ./main.py --experiment Experiment/E19/config$i --jb Experiment/E19/E19.$j/jobs > Experiment/E19/E19.$j/result$i
    done
done
