#!/bin/bash
for i in {1..5}
do
   sbatch --output=1node${i}core-physical.txt --ntasks-per-node=${i} "1nodencore.slurm"
done