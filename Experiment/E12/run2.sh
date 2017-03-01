# This script should be run under the experiment directory. For example Experiment/E9/
cd ../..
for i in {4..9}
do
    for j in {1..12}
    do
        echo algorithm $i runnning on job base $j
        time ./main.py --experiment Experiment/E12/config$i --jb Experiment/E12/E12.$j/jobs > Experiment/E12/E12.$j/result$i
    done
done
