#!/bin/bash
for i in {1..72}
do
   sbatch --output=1node${i}core-physical.txt --ntasks-per-node=${i} "1node${i}core.slurm"
done