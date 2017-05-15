# This script should be run under the experiment directory. For example Experiment/E9/
cd ../..
for i in {2..4}
do
    for j in {1..24}
    do
        echo algorithm $i runnning on job base $j
        time ./main.py --experiment Experiment/E22/config$i --jb Experiment/E22/E22.$j/jobs > Experiment/E22/E22.$j/result$i
    done
done
