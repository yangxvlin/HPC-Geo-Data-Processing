# HPC-Geo-Data-Processing
COMP90024 Cluster and Cloud Computing - Assignment 1 - 2020S1

## how to run
1. ```pip install -r requirements.txt```
2. run program on computer
```
mpiexec -n numprocs python -m mpi4py pyfile
mpiexec -n 8 python -m mpi4py main.py -grid ../data/melbGrid.json -data ../data/testTwitter.json
mpiexec -n 8 python -m mpi4py main.py -grid ../data/melbGrid.json -data ../data/smallTwitter.json
```
