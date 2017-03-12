# This script should be run under the experiment directory. For example Experiment/E13/
cd ../..
for i in {1..5}
do
    for j in 3 5 10 20
    do
        time ./main.py --experiment Experiment/E15/config$i --jb Experiment/E15/jobs_$j --repeat 10000 > Experiment/E15/result${j}_${i}       
    done
done

