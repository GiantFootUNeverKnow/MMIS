# This script should be executed under /MMIS
c=2
cd Experiment/E4/E4.$c
mkdir jobs
cd ../../..
for i in {1..19}
do
    ./jobs_generator.py --batch --redir PUS$i --jl 400 < Experiment/E4/E4.$c/input/$i.txt
done
cd job_base
mv PUS* ../Experiment/E4/E4.$c/jobs
