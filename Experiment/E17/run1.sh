# This script should be executed under an experiment. For example Experiment/E9
for i in {1..4}
do
    cd E17.$i
    mkdir jobs
    cd ..
done
cd ../..
for i in {1..4}
do
    ./jobs_generator.py --batch --redir E17 --jl 400 < Experiment/E17/E17.$i/input 
    cd job_base/E17
    mv * ../../Experiment/E17/E17.$i/jobs
    cd ../..
done
