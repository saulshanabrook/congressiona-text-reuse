#!/usr/bin/env bash

rm shingles.congress # stores the shingles
rm windows.log # stores the reports of the

# declare -a arr=("/Volumes/bigone/bills/mdenny_copy_early2015/bills/POS_Tagged_Bills/bill91199.anno", "/Volumes/bigone/bills/mdenny_copy_early2015/bills/POS_Tagged_Bills/bill91198.anno")

for item in /Volumes/bigone/bills/mdenny_copy_early2015/bills/POS_Tagged_Bills/bill9111*
do
    python windows.py -fn "$item" -size 100
done
