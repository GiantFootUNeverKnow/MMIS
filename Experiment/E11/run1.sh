# This script should be run under the experiment directory. For example Experiment/E11/
cd ../..
for i in {1..10}
do
        time ./main.py --experiment Experiment/E11/config$i --jb Experiment/E11/jobs --repeat 10000 > Experiment/E11/result$i
done
