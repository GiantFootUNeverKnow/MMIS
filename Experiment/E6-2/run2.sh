# This script should be executed under /MMIS
for i in {1..19}
do
    ./main.py --experiment Experiment/E6-2/config --jb Experiment/E6-2/jobs/PPS$i  > Experiment/E6-2/result$i
done
cd Experiment/E6-2
mkdir b
mv result* b
mv b result

