import json
import psutil
import os
import time
import numpy as np
import multiprocessing

from quantumcircuit import QuantumCircuit
from simulator import GKSimulator
from observables import PauliObservables
from grading.utils import *
# inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


# decorator function
def profile(func):
    def wrapper(*args, **kwargs):
        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        print("{}: consumed memory: {:,}".format(
            func.__name__,
            mem_before, mem_after, mem_after - mem_before))

        return result

    return wrapper

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # MB


def chunk_list(data, n_chunks):
    """Split the data into n_chunks."""
    chunk_size = len(data) // n_chunks + (len(data) % n_chunks > 0)
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def run_multiple(circuit_list):
    r = []
    for circuit in circuit_list:
        print(circuit)
        q = QuantumCircuit(circuit)
        s = GKSimulator(q)
        r.append(s.run(q))

    return r 

n_cores = 8

def run_multiprocessing(circuit_list, n_cores):
    """Run the run_multiple function in parallel.    written with ChatGPT"""
    # Split the circuit list into chunks
    chunks = chunk_list(circuit_list, n_cores)

    # Create a multiprocessing pool
    with multiprocessing.Pool(n_cores) as pool:
        # Distribute chunks to the pool
        results = pool.map(run_multiple, chunks)

    # Flatten the list of results
    flattened_results = [item for sublist in results for item in sublist]
    return flattened_results

@profile
def main():
    with open('grading/grading_circuits.json', 'r') as file:
        circuits_to_simulate = json.load(file)

    with open('grading/results.json', 'r') as file:
        results = json.load(file)

    start_time = time.perf_counter()

    runs = run_multiprocessing(circuits_to_simulate, n_cores)

    end_time = time.perf_counter()

    print("Homework Results: ", runs)
    print("Actual Results: ", results)
    print(f'Grade: {compare_results(runs, results)} out of {len(circuits_to_simulate)}.')
    print(f"Elapsed time: {end_time - start_time} seconds")


if __name__ == '__main__':
    main()
