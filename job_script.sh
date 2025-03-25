#!/bin/bash
#SBATCH --job-name=streamjob
#SBATCH --output=streamjob.out
#SBATCH --error=streamjob.err
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --gpus-per-task=1
#SBATCH --time=30
#SBATCH -C gpu
#SBATCH -A nstaff
#SBATCH -q regular

module load PrgEnv-nvidia

JOBID=${SLURM_JOB_ID}
if [[ -z "$JOBID" ]]; then
    echo "Error: JOBID is empty or invalid" >&2
    exit 1
fi

mkdir -p ${JOBID}

srun --ntasks-per-node=4 --gpus-per-task=1 bash -c 'node_name=$(hostname | tr -c "[:alnum:]" "_"); ./cuda-stream &> '${JOBID}'/${node_name}.out'
