from simulator import GKSimulator
import psutil
import os
import time

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # MB


if __name__ == "__main__":  # code aussi généré par l'IA, car pour le multiprocess ça le demande
    simulator = GKSimulator()

    mem_before = get_memory_usage()
    start_time = time.perf_counter()
    # Simulation séquentielle
    resultats = simulator.simuler("fichier_json.json")
    print("Résultats  :", resultats)
    end_time = time.perf_counter()
    mem_after = get_memory_usage()

    print(f"Memory usage: {mem_after - mem_before} MB")
    print(f"Elapsed time: {end_time - start_time} seconds")
