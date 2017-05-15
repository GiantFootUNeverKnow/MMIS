# This script should be executed under an experiment. For example Experiment/E9
for i in {1..24}
do
    cd E22.$i
    mkdir jobs
    cd ..
done
cd ../..
for i in {1..24}
do
    ./jobs_generator.py --batch --redir E22 --jl 100 < Experiment/E22/E22.$i/input 
    cd job_base/E22
    mv * ../../Experiment/E22/E22.$i/jobs
    cd ../..
done
