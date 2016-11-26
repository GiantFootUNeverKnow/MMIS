c=9
cd Experiment/E2/E2.$c
mkdir jobs
cd ../../..
for i in {1..19}
do
    ./jobs_generator.py --batch --redir PUS$i --jl 400 < Experiment/E2/E2.$c/input/$i.txt
done
cd job_base
mv PUS* ../Experiment/E2/E2.$c/jobs
