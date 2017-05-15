# This file is used in a directory of experiment. E.g. E20
for i in {1..12}
do
    mv E20.$i E22.$((i + 12))     
done
rm E20*/result*
