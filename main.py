import json
import psutil
import os
import time

from quantumcircuit import QuantumCircuit
from simulator import GKSimulator


def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # MB


if __name__ == '__main__':
    with open('dummy_circuits.json', 'r') as file:
        l = json.load(file)

    q = QuantumCircuit(l)
    s = GKSimulator()

    mem_before = get_memory_usage()
    start_time = time.perf_counter()
    r = s.run(q)
    end_time = time.perf_counter()
    mem_after = get_memory_usage()
    
    print(r)

    print(f"Memory usage: {mem_after - mem_before} MB")
    print(f"Elapsed time: {end_time - start_time} seconds")
