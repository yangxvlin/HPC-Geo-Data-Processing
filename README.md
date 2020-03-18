# HPC-Geo-Data-Processing
COMP90024 Cluster and Cloud Computing - Assignment 1 - 2020S1

## Contributors
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
<table>
  <tr>
  </tr>
</table>

## how to run
1. ```pip install -r requirements.txt```
2. run program on computer
```
mpiexec -n numprocs python -m mpi4py pyfile
mpiexec -n 8 python -m mpi4py main.py -grid ../data/melbGrid.json -data ../data/testTwitter.json
mpiexec -n 8 python -m mpi4py main.py -grid ../data/melbGrid.json -data ../data/smallTwitter.json
```
