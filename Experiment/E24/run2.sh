# This script should be run under the experiment directory. For example Experiment/E9/

cd ../..
for i in {11..12}
do
    for j in PUS2_1k PES1_1k 
    do
        echo algorithm $i runnning on job base $j 
        time ./main.py --experiment Experiment/E24/config$i --jb Experiment/E24/$j > Experiment/E24/result${i}_$j
    done
done
for i in {1..3}
do
    for j in PUS1_10k PES1_10k 
    do
        echo algorithm $i runnning on job base $j
        time ./main.py --experiment Experiment/E24/config$i --jb Experiment/E24/$j > Experiment/E24/result${i}_$j
    done
done
