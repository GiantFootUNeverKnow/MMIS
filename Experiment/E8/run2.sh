# This script should be executed under /MMIS
name='PNS'
for i in {1..19}
do
    ./main.py --experiment Experiment/E8/config --jb Experiment/E8/jobs$name/$name$i  > Experiment/E8/result$i
done
cd Experiment/E8
mkdir b
mv result* b
mv b result$name

