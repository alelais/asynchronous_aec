#!/usr/bin/env sh
#SBATCH --exclude scuderi

srun -u python3 asynchronous.py "$@"
