#!/bin/bash
#SBATCH --mail-user=xuliny@student.unimelb.edu.au
#SBATCH --mail-type=End
#SBATCH --output=run.txt

for i in {1..72}
do
   sbatch --output=1node${i}core-physical.txt --ntasks-per-node=${i} --partition=physical --nodes=1 "1nodencore.slurm"
#   sbatch --output=1node${i}core-cloud.txt --ntasks-per-node=${i} --partition=cloud --nodes=1 "1nodencore.slurm"
done

for i in {1..36}
do
   sbatch --output=2node$(i*2)core-physical.txt --ntasks-per-node=${i} --partition=physical --nodes=2 "1nodencore.slurm"
   sbatch --output=2node$(i*2)core-cloud.txt --ntasks-per-node=${i} --partition=cloud --nodes=2 "1nodencore.slurm"
done