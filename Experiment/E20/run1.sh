# This script should be executed under an experiment. For example Experiment/E9
for i in {1..12}
do
    cd E20.$i
    mkdir jobs
    cd ..
done
cd ../..
for i in {1..12}
do
    ./jobs_generator.py --batch --redir E20 --jl 100 < Experiment/E20/E20.$i/input 
    cd job_base/E20
    mv * ../../Experiment/E20/E20.$i/jobs
    cd ../..
done
