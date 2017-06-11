# This script should be executed under an experiment. For example Experiment/E9
for i in {1..24}
do
    cd E25.$i
    mkdir jobs
    cd ..
done
cd ../..
for i in {1..24}
do
    ./jobs_generator.py --batch --redir E25 --jl 100 < Experiment/E25/E25.$i/input 
    cd job_base/E25
    mv * ../../Experiment/E25/E25.$i/jobs
    cd ../..
done
