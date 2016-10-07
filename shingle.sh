#!/usr/bin/env bash

for (( i=1; i <= 3; i++ ))
do
    python pi.py  # make pi
    for item in bills/*
    do
        echo "$i $item"
    done    
done