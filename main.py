"""
WARNING: WHILE THE MAJORITY OF THIS WORK WAS INDEPENDENTLY IMPLEMENTED BY THE AUTHOR, LARGE LANGUAGE MODELS (LLMS) WERE UTILIZED THROUGHOUT THE PROJECT, PRIMARILY FOR AUTO-COMPLETION OF CODE OR COMMENTS. This module simulates Clifford circuits efficiently using the stabilizer formalism.
"""

import json
import os
import time

import psutil

from quantumcircuit import QuantumCircuit
from simulator import GKSimulator


def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # MB


if __name__ == "__main__":
    with open("dummy_circuits.json", "r") as file:
        l = json.load(file)

    q = QuantumCircuit(l)
    s = GKSimulator()

    mem_before = get_memory_usage()
    start_time = time.perf_counter()
    r = s.run(q)
    end_time = time.perf_counter()
    mem_after = get_memory_usage()

    print(f"Memory usage: {mem_after - mem_before} MB")
    print(f"Elapsed time: {end_time - start_time} seconds")
