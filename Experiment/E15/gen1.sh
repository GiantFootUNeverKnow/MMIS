# This script should be executed under an experiment. For example Experiment/E15
cd ../..
C=(25 24 20 15 14 10)
L=(1.5 1.618 2.0 3.0 3.1415 4.0)
for i in 2 3 5 10 20
do
    for j in {0..5}
    do
        echo 6 >> input 
        echo ${C[$j]} >> input
        echo ${L[$j]} >> input
        echo $i >> input
        if [ $j -eq 5 ]
        then echo Y >> input
        else echo N >> input
        fi
    done
    ./jobs_generator.py --redir jobs_$i < input
    rm input
              
    cd job_base 
    mv jobs_$i ../Experiment/E15
    cd ..
done
