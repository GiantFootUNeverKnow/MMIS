# This script should be executed under an experiment. For example Experiment/E9
for i in {1..12}
do
    cd E14.$i
    mkdir jobs
    cd ..
done
cd ../..
for i in {1..12}
do
    ./jobs_generator.py --batch --redir E14 --jl 100 < Experiment/E14/E14.$i/input 
    cd job_base/E14
    mv * ../../Experiment/E14/E14.$i/jobs
    cd ../..
done
