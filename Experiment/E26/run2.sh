# This script should be run under the experiment directory. For example Experiment/E9/
cd ../..
    for j in {1..12}
    do
        echo runnning on job base $j
        time ./main.py --experiment Experiment/E26/config --jb Experiment/E26/E26.$j/jobs > Experiment/E26/E26.$j/result
    done
