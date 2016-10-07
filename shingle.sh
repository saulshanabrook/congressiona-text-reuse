#!/usr/bin/env bash

HASH_LEN=32

for (( i=1; i <= 3; i++ ))
do
    python pi.py  # make pi
    for item in bills/*
    do
        echo "$i $item $HASH_LEN"
    done    
done