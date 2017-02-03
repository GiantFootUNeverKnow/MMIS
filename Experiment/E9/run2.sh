# This script should be run under the experiment directory. For example Experiment/E9/
cd ../..
for i in {2..3}
do
    for j in {1..12}
    do
        ./main.py --experiment Experiment/E9/config$i --jb Experiment/E9/E9.$j/jobs --repeat 100 > Experiment/E9/E9.$j/result$i
    done
done
