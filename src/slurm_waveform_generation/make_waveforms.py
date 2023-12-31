"""Make N waveforms for a given prior file and save to a h5 file"""
import argparse
import bilby
import os
from tqdm.auto import tqdm
from time import process_time
import numpy as np
import pandas as pd
import h5py


def get_cli_args():
    """Get the n and prior file from the command line"""
    parser = argparse.ArgumentParser(
        description="Make N waveforms for a given prior file"
    )
    parser.add_argument(
        "-n", "--n_waveforms", type=int, required=True, help="Number of waveforms to make"
    )
    parser.add_argument(
        "-p",
        "--prior_file",
        type=str,
        required=True,
        help="Path to the prior file to use",
    )
    parser.add_argument(
        "-o",
        "--outdir",
        type=str,
        required=True,
        help="Path to the output directory",
    )
    args = parser.parse_args()

    if not os.path.exists(args.prior_file):
        raise ValueError(f"Prior file {args.prior_file} does not exist")


def run_waveform_generator(n_waveforms: int, prior_file: str, outfn: str):
    prior = bilby.core.prior.PriorDict.from_file(prior_file)
    samples = prior.sample(n_waveforms)

    # make a tqdm pbar to track progress
    pbar = tqdm(total=n_waveforms, desc="Making waveforms")
    start = process_time()

    waveforms = []
    runtimes = np.zeros(n_waveforms)

    for i in pbar:
        # add total-mass to the pbar post
        pbar.set_postfix({"total_mass": round(samples[i]["total_mass"], 2)})

        # generate waveform
        t0 = process_time()
        waveforms.append(__generate_waveform(**samples[i]))
        t1 = process_time()
        runtimes[i] = t1 - t0

    waveforms = convert_lists_of_different_sizes_to_np_ndarray(waveforms)
    samples = pd.DataFrame(samples)
    samples["runtime"] = runtimes
    # write waveforms and samples to h5 file
    with h5py.File(outfn, "w") as f:
        f.create_dataset("waveforms", data=waveforms)
        samples.to_hdf(f, "samples")

    end = process_time()
    print(f"Time taken: {end - start:.2f} s")


def convert_lists_of_different_sizes_to_np_ndarray(data):
    """Convert a list of lists of different sizes to a numpy ndarray padded with nans

    :param data: List of lists of different sizes
    :return: Numpy ndarray
    """
    max_shape = max([np.array(d).shape for d in data])
    padded_data = np.full((len(data), *max_shape), np.nan)
    for i, d in enumerate(data):
        padded_data[i, : len(d)] = d
    return padded_data


def __generate_waveform(**kwargs) -> np.ndarray:
    """Given waveform parameters, generate the waveform h+ and hx and return it as a numpy array"""
    return np.zeros((2, 1000))
