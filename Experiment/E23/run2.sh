# This script should be run under the experiment directory. For example Experiment/E9/
cd ../..
for i in {4..12}
do
    for j in {1..9}
    do
        echo algorithm $i runnning on job base $j
        time ./main.py --experiment Experiment/E23/config$i --jb Experiment/E23/E23.$j/jobs > Experiment/E23/E23.$j/result$i
    done
done
for i in {1..3}
do
    for j in {10..18}
    do
        echo algorithm $i runnning on job base $j
        time ./main.py --experiment Experiment/E23/config$i --jb Experiment/E23/E23.$j/jobs > Experiment/E23/E23.$j/result$i
    done
done
