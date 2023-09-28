import os
from typing import List


from .file_generators import make_slurm_file
from .slurm_utils import mkdir


MAX_ARRAY_SIZE = 2048


def setup_jobs(
    n_waveforms: int,
    prior_file: str,
    n_array_jobs: int,
    outdir: str,
    module_loads: str,
    submit: bool,
    clean: bool,
    email: str = "",
    partition: str = "",
) -> None:
    """
    Generate slurm files for generating waveforms and saving them
    """
    print(f"Generating slurm files for waveform generation using prior file {prior_file}")
    submit_dir = mkdir(outdir, "submit")

    waveforms_per_batch = n_waveforms // n_array_jobs
    assert n_array_jobs <= MAX_ARRAY_SIZE, f"Array size must be <= {MAX_ARRAY_SIZE}"


    kwargs = dict(
        outdir=outdir,
        module_loads=module_loads,
        submit_dir=submit_dir,
        email=email,
    )

    out_fname = os.path.join(outdir, "waveforms", "waveform_0.h5")
    cmd = f"srun make_waveforms -n {waveforms_per_batch} -o {outdir} -p {prior_file}"
    cmd += f"--outdir {outdir} "
    common_array_kwargs = dict(
        **kwargs,
        jobid=i,
        array_job=True,
    )


    submit_file = make_slurm_file(
        **common_array_kwargs,
        cpu_per_task=1,
        time="20:00",
        jobname=f"gen",
        mem="1000MB",
        command=f"{cmd} --setup",
    )
    print(f"To run job:\n>>> sbatch {submit_file}")


