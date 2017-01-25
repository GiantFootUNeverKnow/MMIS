# This script should be executed under an experiment. E.g. Experiment/E4
mkdir input
for i in {1..19}
do
    k=`echo $i \* 0.05 | bc -l`
    echo "3" > input/$i.txt
    echo "$k" >> input/$i.txt
    echo "20" >> input/$i.txt
    echo "lambda y: y*y" >> input/$i.txt
    echo "100" >> input/$i.txt
    echo "Y" >> input/$i.txt
done
