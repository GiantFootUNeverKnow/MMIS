# This script should be executed under an experiment. E.g. Experiment/E4

a=5
b=25
c=2
cp clip.py E4.$c
cd E4.$c
mkdir input
cd ..
for i in {1..19}
do
    k=`echo $i \* 0.05 | bc -l`
    echo "1" > E4.$c/input/$i.txt
    echo "$k" >> E4.$c/input/$i.txt
    echo "$a" >> E4.$c/input/$i.txt
    echo "$b" >> E4.$c/input/$i.txt
    echo "lambda y:y * y" >> E4.$c/input/$i.txt
    echo "100" >> E4.$c/input/$i.txt
    echo "Y" >> E4.$c/input/$i.txt
done
