# This file is used in a directory of experiment. E.g. E20
for i in {1..24}
do
    mv E22.$i E25.$((i))     
done
rm E25*/result*
