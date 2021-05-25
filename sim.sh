#!/bin/bash
cd python
output_file="../results.txt"

for ham in nh3_bk
do
  for i in {1..3}
  do
    printf "ham=$ham, repetition=$i" >> $output_file
    printf "\n" >> $output_file
    python sim.py $ham >> $output_file
    printf "\n" >> $output_file
  done
done
