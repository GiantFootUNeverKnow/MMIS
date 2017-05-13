# This script should be executed under an experiment. For example Experiment/E15
cd ../..
C=(15 22 18)
L1=(2.0 2.0 4.0)
L2=(4 1.5 1.5)

for j in {0..2}
do
    echo 7 >> input 
    echo ${C[$j]} >> input
    echo 2 >> input
    echo ${L1[$j]} >> input
    echo ${L2[$j]} >> input
    echo 10000 >> input
    echo Y >> input
   
    ./jobs_generator.py --batch --redir jobs_$j < input
    rm input
              
    cd job_base 
    mv jobs_$j ../Experiment/E21
    cd .. 
done
