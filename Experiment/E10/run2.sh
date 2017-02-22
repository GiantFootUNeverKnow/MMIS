# This script should be run under the experiment directory. For example Experiment/E9/
cd ../..
for i in {1..3}
do
    for j in {1..12}
    do
        time ./main.py --experiment Experiment/E10/config$i --jb Experiment/E10/E10.$j/jobs > Experiment/E10/E10.$j/result$i
    done
done
