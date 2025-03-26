#!/bin/bash
#SBATCH -C gpu
#SBATCH -q debug
#SBATCH -A nstaff
#SBATCH -t 00:30:00
#SBATCH -N 4
#SBATCH --gpus-per-task=1
#SBATCH --ntasks-per-node=4
#SBATCH --job-name=dgemmjob
#SBATCH --output=dgemmjob.out
#SBATCH --error=dgemmjob.err
#SBATCH --exclusive

HOME="$(pwd)"

module load python

JOBID=${SLURM_JOB_ID}
if [[ -z "$JOBID" ]]; then
    echo "Error: JOBID is empty or invalid" >&2
    exit 1
fi

mkdir -p ${HOME}/${JOBID}

srun --gpus-per-task 1 --ntasks-per-node 4 bash -c 'node_name=$(hostname | tr -c "[:alnum:]" "_"); '$HOME'/python-dgemm.py --nsize 4096 --accelerator >> '${HOME}'/'${JOBID}'/${node_name}.out 2>&1'


