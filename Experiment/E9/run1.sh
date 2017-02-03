# This script should be executed under an experiment. For example Experiment/E9
for i in {1..12}
do
    cd E9.$i
    mkdir jobs
    cd ..
done
cd ../..
for i in {1..12}
do
    ./jobs_generator.py --batch --redir E9 --jl 400 < Experiment/E9/E9.$i/input 
    cd job_base/E9
    mv * ../../Experiment/E9/E9.$i/jobs
    cd ../..
done
