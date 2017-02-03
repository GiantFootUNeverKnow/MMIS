# This script should be executed under an experiment. E.g. Experiment/E4
name='PNS'
mkdir input$name
for i in {1..19}
do
    k=`echo $i \* 0.05 | bc -l`
    echo "5" > input$name/$i.txt
    echo "$k" >> input$name/$i.txt
    echo "10" >> input$name/$i.txt
    echo "3" >> input$name/$i.txt
    echo "lambda y: y*y" >> input$name/$i.txt
    echo "100" >> input$name/$i.txt
    echo "Y" >> input$name/$i.txt
done
