import sys

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

cache_sizes_in_KB = {"cortex_a15": [2, 4, 8, 16, 32], "cortex_a7": [1, 2, 4, 8, 16]}


def get_simple_scalar_config_for_cache_size(
    il1_cache_size, dl1_cache_size, processor_config, block_size=64
):
    return (
        f"-cache:il1 il1:{int(1024 * il1_cache_size / block_size)}:{block_size}:2:l "
        + f"-cache:dl1 dl1:{int(1024 * dl1_cache_size / block_size)}:{block_size}:2:l "
        + processor_config
    )


if len(sys.argv) <= 2:
    raise Exception(
        (
            "Not enough arguments. Command: ./generate_commands.py [processor: cortex_a15 or cortex_a7] [paths_to_executables]"
            + "\nExample: ./generate_commands.py cortex_a15 myapp.ss"
            + "\n ./generate_commands.py cortex_a7 myapp1.ss myapp2.ss"
        )
    )

processor = sys.argv[1]
if processor not in ["cortex_a15", "cortex_a7"]:
    raise Exception("Invalid processor type, possible options: cortex_a15 or cortex_a7")

executables = " ".join(sys.argv[2:])

print(f"Processor: {processor}, executables: {executables}")


for cache_size in cache_sizes_in_KB[processor]:
    config = get_simple_scalar_config_for_cache_size(
        il1_cache_size=cache_size,
        dl1_cache_size=cache_size,
        processor_config=PROCESSOR_CONFIG[processor],
    )
    command = "sim-outorder " + " ".join([config, executables])
    print(f"\nil1: {cache_size}KB, dl1: {cache_size}KB\n{command}")
