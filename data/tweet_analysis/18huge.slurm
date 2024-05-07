#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --partition=sapphire
#SBATCH --time=01:00:00

module purge
module load foss/2022a
module load Python/3.10.4
module load mpi4py/3.1.4
module load SciPy-bundle/2022.05

pip install ijson

srun -n 8 python3 run-seek.py twitter-100gb.json eight

##DO NOT ADD/EDIT BEYOND THIS LINE##
##Job monitor command to list the resource usage
my-job-stats -a -n -s

