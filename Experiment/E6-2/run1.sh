# This script should be executed under an experiment. For example Experiment/E6
mkdir jobs
cd ../..
for i in {1..19}
do
    ./jobs_generator.py --batch --redir PPS$i --jl 400 < Experiment/E6-2/input/$i.txt
done
cd job_base
mv PPS* ../Experiment/E6-2/jobs
