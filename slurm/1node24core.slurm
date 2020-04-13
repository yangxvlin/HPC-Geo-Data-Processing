#!/bin/bash

#SBATCH --account=COMP90024
#SBATCH --partition=physical
#SBATCH --output=1node24core-physical.txt
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --mail-user=xuliny@student.unimelb.edu.au
#SBATCH --mail-type=End
#SBATCH --time=1-0:0:00

# Run the job from this directory:
cd /home/$USER/COMP90024/HPC-Geo-Data-Processing/slurm
# The modules to load:
module load Python/3.6.1-intel-2017.u2

# The job command(s):
time mpirun python3 "../src/main.py" -country "../src/language.json" -data "../data/bigTwitter.json"
