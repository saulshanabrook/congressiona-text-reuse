#!/usr/bin/env bash

# check a file to see if it is an interesting pair (two docs)
# if not, delete!

COUNT=$(awk -F, '{print $1}' $1 | sort | uniq | wc -l)

echo $COUNT

if [ $COUNT -eq 1 ]
  then
  rm $1
fi