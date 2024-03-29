# -*- coding: utf-8 -*-
"""ES201 - TD4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zeLsaRtpZfSs0LDQwL7C55Vevmyl3l5l
"""

import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

os.system("rm -rf plots && mkdir plots")

PROCESSOR_CONFIG = {
    "cortex_a15": (
        "-bpred:2lev 256  -fetch:ifqsize 8 -fetch:mplat 15 "
        + "-decode:width 4 -issue:width 8 -commit:width 4 -ruu:size 16 -lsq:size 16 -res:ialu 5 -res:fpalu 1 -res:imult 1 -res:fpmult 1 "
    ),
    "cortex_a7": (
        "-bpred:bimod 256  -fetch:ifqsize 4 -fetch:mplat 8 "
        + "-decode:width 2 -issue:width 4 -commit:width 2 -ruu:size 2 -lsq:size 8 -res:ialu 1 -res:fpalu 1 -res:imult 1 -res:fpmult 1 "
    ),
}

DEFAULT_CACHE_SIZE_IN_KB = 32

cache_sizes_in_KB = {"cortex_a15": [2, 4, 8, 16, 32], "cortex_a7": [1, 2, 4, 8, 16]}

metric_names = [
    ("sim_IPC", "instructions per cycle"),
    ("sim_CPI", "cycles per instruction"),
    ("bpred_bimod.misses", "total number of misses"),
    ("il1.miss_rate", "il1 miss rate"),
    ("dl1.miss_rate", "dl1 miss rate"),
    ("ul2.miss_rate", "ul2 miss rate"),
]

metric_labels = np.array(metric_names)[:, 1]


def get_simple_scalar_config_for_cache_size(
    il1_cache_size, dl1_cache_size, processor_config, block_size=64
):
    return (
        f"sim-outorder -cache:il1 il1:{int(1024 * il1_cache_size / block_size)}:{block_size}:2:l "
        + f"-cache:dl1 dl1:{int(1024 * dl1_cache_size / block_size)}:{block_size}:2:l "
        + processor_config
    )


def plot_metrics(cache_size, metrics, metric_labels, x_label, file_prefix):
    metrics = np.transpose(metrics)
    for m, m_name in zip(metrics, metric_labels):
        plt.bar(cache_size, m)
        plt.xlabel(x_label)
        plt.ylabel(m_name)
        plt.show()
        fig = plt.gcf()
        fig.savefig(f"./plots/{file_prefix}-{m_name}.png")


def get_numeric_value(str):
    result = re.findall("\d+\.*\d+", str)

    if len(result) == 0:
        raise Exception(f"Cannot find match for numeric value in {str}")
    if len(result) > 1:
        raise Exception(f"More than 1 match for numeric value in {str}")

    return float(result[0])


def get_metrics_values(output):
    metrics = []

    for metric, _ in metric_names:
        pattern = f"{metric}[\s]*[\d]+[\.]?[\d]+"
        result = re.findall(pattern, output)

        if len(result) == 0:
            raise Exception(f"Cannot find match for {metric}")
        if len(result) > 1:
            raise Exception(f"More than 1 match for {metric}: ", result)

        metric_value = get_numeric_value(result[0])
        metrics.append(metric_value)

    return metrics


if len(sys.argv) <= 2:
    raise Exception(
        (
            "Not enough arguments. Command: ./cache_metrics.py [processor: cortex_a15 or cortex_a7] [paths_to_executables]"
            + "\nExemple: ./cache_metrics.py cortex_a15 myapp.ss"
            + "\n ./cache_metrics.py cortex_a7 myapp1.ss myapp2.ss"
        )
    )

processor = sys.argv[1]
if processor not in ["cortex_a15", "cortex_a7"]:
    raise Exception("Invalid processor type, possible options: cortex_a15 or cortex_a7")

executables = " ".join(sys.argv[2:])

print(f"Processor: {processor}, executables: {executables}")

# Change DL1 cache size

all_metrics = []

for dl1 in cache_sizes_in_KB[processor]:
    config = get_simple_scalar_config_for_cache_size(
        il1_cache_size=32,
        dl1_cache_size=dl1,
        processor_config=PROCESSOR_CONFIG[processor],
    )
    output = subprocess.run(
        ["sim-outorder", " ".join([config, executables])], capture_output=True
    )
    metrics = get_metrics_values(output)
    all_metrics.append(metrics)

plot_metrics(
    cache_sizes_in_KB[processor],
    all_metrics,
    metric_labels,
    x_label="La taille du cache DL1",
    file_prefix=f"il1={DEFAULT_CACHE_SIZE_IN_KB}KB-dl1={dl1}KB",
)

# Change IL1 cache size

all_metrics = []

for il1 in cache_sizes_in_KB[processor]:
    config = get_simple_scalar_config_for_cache_size(
        il1_cache_size=32,
        dl1_cache_size=dl1,
        processor_config=PROCESSOR_CONFIG[processor],
    )
    output = subprocess.run(
        ["sim-outorder", " ".join([config, executables])], capture_output=True
    )
    metrics = get_metrics_values(output)
    all_metrics.append(metrics)

plot_metrics(
    cache_sizes_in_KB[processor],
    all_metrics,
    metric_labels,
    x_label="La taille du cache IL1",
    file_prefix=f"il1={il1}KB-dl1={DEFAULT_CACHE_SIZE_IN_KB}KB",
)

print("\nPlots have been generated successfully")

os.system("zip -r plots.zip plots")

print(
    "\nPlots have been archived to plots.tar.gz. You can now upload this file to your git repo."
)
