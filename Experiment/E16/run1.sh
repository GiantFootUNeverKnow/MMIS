# This script should be executed under an experiment. For example Experiment/E9
for i in {1..18}
do
    cd E16.$i
    mkdir jobs
    cd ..
done
cd ../..
for i in {1..18}
do
    ./jobs_generator.py --batch --redir E16 --jl 100 < Experiment/E16/E16.$i/input 
    cd job_base/E16
    mv * ../../Experiment/E16/E16.$i/jobs
    cd ../..
done
