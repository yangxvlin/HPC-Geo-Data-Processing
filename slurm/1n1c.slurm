#!/bin/bash

#SBATCH --account=COMP90024
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1-0:0:00

# check that the script is launched with sbatch
if [ "x$SLURM_JOB_ID" == "x" ]; then
   echo "You need to submit your job to the queuing system with sbatch"
   exit 1
fi

# Run the job from this directory:
cd /home/$USER/COMP90024/HPC-Geo-Data-Processing/slurm
# The modules to load:
module load MPICH/3.2.1-GCC-6.2.0
module load Python/3.5.2-GCC-6.2.0

# The job command(s):
time mpirun python3 "../src/main.py" -data "../../../../../data/projects/COMP90024/bigTwitter.json"
