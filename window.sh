#!/usr/bin/env bash

rm shingles.congress # stores the shingles
rm windows.log # stores the reports of the

echo 'fn,digit,window_no,window_size,iter' > shingles.congress


# for item in /Volumes/bigone/bills/mdenny_copy_early2015/bills/POS_Tagged_Bills/bill911*

for (( c=1; c<=100; c++ ))
do
    echo "$c"
    python pi.py
    for item in demos/*.anno
    do
        python windows.py -fn "$item" -window_size 5 -iter "$c"
    done
done
