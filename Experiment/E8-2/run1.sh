# This script should be executed under an experiment. For example Experiment/E6
name='PES'
mkdir jobs$name
cd ../..
for i in {1..19}
do
    ./jobs_generator.py --batch --redir $name$i --jl 400 < Experiment/E8-2/input$name/$i.txt
done
cd job_base
mv $name* ../Experiment/E8-2/jobs$name
