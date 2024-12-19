import psutil
import os
import time
import json

from quantumcircuit import QuantumCircuit
from simulator import GKSimulator



def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss



def profile(func):
    def wrapper(*args, **kwargs):
        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        print("{}: mémoire consommée : {:,}".format(
            func.__name__,
            mem_after - mem_before))
        return result

    return wrapper


@profile
def main():
   
    with open('dummy_circuits.json', 'r') as file:
        circuits_to_simulate = json.load(file)


    q = QuantumCircuit(circuits_to_simulate)
    sim = GKSimulator(q)  

    
    start_time = time.perf_counter()
    runs = sim.run()
    end_time = time.perf_counter()

   
    print("Résultats du devoir : ", runs)
    print(f"Temps écoulé : {end_time - start_time} secondes")
