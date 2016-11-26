a=1
b=125
c=9
cp clip.py E2.$c
cd E2.$c
mkdir input
cd ..
for i in {1..19}
do
    k=`echo $i \* 0.05 | bc -l`
    echo "1" > E2.$c/input/$i.txt
    echo "$k" >> E2.$c/input/$i.txt
    echo "$a" >> E2.$c/input/$i.txt
    echo "$b" >> E2.$c/input/$i.txt
    echo "lambda y:y * y * y" >> E2.$c/input/$i.txt
    echo "100" >> E2.$c/input/$i.txt
    echo "Y" >> E2.$c/input/$i.txt
done
