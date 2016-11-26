c=9
for i in {1..19}
do
    ./main.py --experiment Experiment/E2/E2.$c/config --jb Experiment/E2/E2.$c/jobs/PUS$i  > Experiment/E2/E2.$c/result$i
done
cd Experiment/E2/E2.$c
mkdir b
mv result* b
mv b result

