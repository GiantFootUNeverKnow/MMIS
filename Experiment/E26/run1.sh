# This script should be executed under an experiment. For example Experiment/E9
for i in {1..12}
do
    cd E26.$i
    mkdir jobs
    cd ..
done
cd ../..
for i in {1..12}
do
    ./jobs_generator.py --batch --redir E26 --jl 150 < Experiment/E26/E26.$i/input 
    cd job_base/E26
    mv * ../../Experiment/E26/E26.$i/jobs
    cd ../..
done
