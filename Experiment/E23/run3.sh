# This file is used in a directory of experiment. E.g. E20
for i in {1..18}
do
    mv E16.$i E23.$((i))     
done
rm E16*/result*
