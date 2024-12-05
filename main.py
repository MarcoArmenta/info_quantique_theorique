import json
import psutil
import os
import time
import numpy as np
import multiprocessing

from quantumcircuit import QuantumCircuit
from simulator import GKSimulator
from observables import PauliObservables

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

if __name__ == '__main__':
    with open('dummy_circuits.json', 'r') as file:
        l = json.load(file)

    

    mem_before = get_memory_usage()
    start_time = time.perf_counter()

    r = run_multiprocessing(l, n_cores)
    print(r)

    end_time = time.perf_counter()
    mem_after = get_memory_usage()

    print(f"Memory usage: {mem_after - mem_before} MB")
    print(f"Elapsed time: {end_time - start_time} seconds")
