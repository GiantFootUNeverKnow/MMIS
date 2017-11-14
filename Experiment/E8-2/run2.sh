# This script should be executed under /MMIS
name='PES'
for i in {1..19}
do
    ./main.py --experiment Experiment/E8-2/config --jb Experiment/E8-2/jobs$name/$name$i  > Experiment/E8-2/result$i
done
cd Experiment/E8-2
mkdir b
mv result* b
mv b result$name

