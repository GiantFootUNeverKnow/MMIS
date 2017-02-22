# This script should be executed under an experiment. For example Experiment/E9
for i in {1..12}
do
    cd E10.$i
    mkdir jobs
    cd ..
done
cd ../..
for i in {1..12}
do
    ./jobs_generator.py --batch --redir E10 --jl 400 < Experiment/E10/E10.$i/input 
    cd job_base/E10
    mv * ../../Experiment/E10/E10.$i/jobs
    cd ../..
done
