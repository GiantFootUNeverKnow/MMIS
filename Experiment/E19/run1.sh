# This script should be executed under an experiment. For example Experiment/E9
for i in {1..12}
do
    cd E19.$i
    mkdir jobs
    cd ..
done
cd ../..
for i in {1..12}
do
    ./jobs_generator.py --batch --redir E19 --jl 100 < Experiment/E19/E19.$i/input 
    cd job_base/E19
    mv * ../../Experiment/E19/E19.$i/jobs
    cd ../..
done
