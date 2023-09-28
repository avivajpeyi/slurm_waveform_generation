#!/usr/bin/env python

"""CLI for creating slurm jobs

"""

import argparse
import os

from .slurm_job_generator import setup_jobs

PROG = "make_slurm_jobs"

def main():
    parser = argparse.ArgumentParser(
        description="Create slurm job for generation of waveforms",
        prog=PROG,
        usage=f"{PROG} ",
    )

    parser.add_argument(
        "--outdir",
        help=(
            "outdir for jobs. "
        ),
        default="out",
    )
    parser.add_argument(
        "--clean",
        action="store_true",  # False by default
    )
    parser.add_argument(
        "--module_loads",
        default="git/2.18.0 gcc/9.2.0 openmpi/4.0.2 python/3.8.5",
        help="String containing all module loads in one line (each module separated by a space)",
    )
    parser.add_argument(
        "--submit",
        action="store_true",  # False by default
        help="Submit once files created",
    )
    parser.add_argument(
        "--email",
        default="",
        help="email address to send job updates to (default: ''). If not passed, no emails sent.",
    )


    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)


    setup_jobs(
        outdir=args.outdir,
        module_loads=args.module_loads,
        submit=args.submit,
        clean=args.clean,
        email=args.email,
    )

if __name__ == "__main__":
    main()
