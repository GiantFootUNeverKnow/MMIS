# This script should be executed under /MMIS

c=2
for i in {1..19}
do
    ./main.py --experiment Experiment/E4/E4.$c/config1 --jb Experiment/E4/E4.$c/jobs/PUS$i  > Experiment/E4/E4.$c/result1_$i
    ./main.py --experiment Experiment/E4/E4.$c/config2 --jb Experiment/E4/E4.$c/jobs/PUS$i --repeat 50 > Experiment/E4/E4.$c/result2_$i
    ./main.py --experiment Experiment/E4/E4.$c/config3 --jb Experiment/E4/E4.$c/jobs/PUS$i --repeat 50 > Experiment/E4/E4.$c/result3_$i
done
cd Experiment/E4/E4.$c
mkdir b
mv result1_* b
mv b result1
mkdir c
mv result2_* c
mv c result2
mkdir d
mv result3_* d
mv d result3
