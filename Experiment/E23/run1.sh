# This script should be executed under an experiment. For example Experiment/E9
for i in {1..18}
do
    cd E23.$i
    mkdir jobs
    cd ..
done
cd ../..
for i in {1..9}
do
    ./jobs_generator.py --batch --redir E23 --jl 100 < Experiment/E23/E23.$i/input 
    cd job_base/E23
    mv * ../../Experiment/E23/E23.$i/jobs
    cd ../..
done
for i in {10..18}
do
    ./jobs_generator.py --batch --redir E23 --jl 400 < Experiment/E23/E23.$i/input 
    cd job_base/E23
    mv * ../../Experiment/E23/E23.$i/jobs
    cd ../..
done
