# This script should be run under the experiment directory. For example Experiment/E13/
cd ../..
for i in {1..5}
do
        time ./main.py --experiment Experiment/E13/config$i --jb Experiment/E13/jobs2 --repeat 10000 > Experiment/E13/result2_$i        
done
