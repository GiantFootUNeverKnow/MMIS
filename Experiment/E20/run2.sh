# This script should be run under the experiment directory. For example Experiment/E9/
cd ../..
for i in {4..12}
do
    for j in {1..12}
    do
        echo algorithm $i runnning on job base $j
        time ./main.py --experiment Experiment/E20/config$i --jb Experiment/E20/E20.$j/jobs > Experiment/E20/E20.$j/result$i
    done
done
