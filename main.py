import psutil
import os
import time
import json

from quantumcircuit import QuantumCircuit
from simulator import GKSimulator

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


@profile
def main():
    with open('grading/grading_circuits.json', 'r') as file:
        circuits_to_simulate = json.load(file)

    with open('grading/results.json', 'r') as file:
        results = json.load(file)

    q = QuantumCircuit(circuits_to_simulate)
    sim = GKSimulator()

    start_time = time.perf_counter()
    runs = sim.run(q)
    end_time = time.perf_counter()

    print("Homework Results: ", runs)
    print("Actual Results: ", results)
    print(f'Grade: {compare_results(runs, results)} out of {len(circuits_to_simulate)}.')
    print(f"Elapsed time: {end_time - start_time} seconds")


if __name__ == '__main__':
    main()
