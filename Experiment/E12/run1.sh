# This script should be executed under an experiment. For example Experiment/E9
for i in {1..12}
do
    cd E12.$i
    mkdir jobs
    cd ..
done
cd ../..
for i in {1..12}
do
    ./jobs_generator.py --batch --redir E12 --jl 100 < Experiment/E12/E12.$i/input 
    cd job_base/E12
    mv * ../../Experiment/E12/E12.$i/jobs
    cd ../..
done
