import json
import psutil
import os
import time
from quantumcircuit import QuantumCircuit
from simulator import GKSimulator


def get_memory_usage():
    """
    Récupère l'utilisation mémoire actuelle.
    """
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # MB


if __name__ == "__main__":
    # Charger les circuits depuis le fichier JSON
    with open("dummy_circuits.json", "r") as file:
        circuits_data = json.load(file)

    # Initialiser le simulateur
    simulator = GKSimulator()

    # Mesurer l'utilisation mémoire avant la simulation
    mem_before = get_memory_usage()
    start_time = time.perf_counter()

    # Simuler chaque circuit
    results = []
    for circuit_data in circuits_data:
        # Construire un circuit pour chaque ensemble de données
        circuit = QuantumCircuit(circuit_data)

        # Exécuter la simulation
        result = simulator.executer(circuit)
        results.append(result)

    # Mesurer l'utilisation mémoire après la simulation
    end_time = time.perf_counter()
    mem_after = get_memory_usage()

    # Afficher les résultats
    print(f"Memory usage: {mem_after - mem_before:.2f} MB")
    print(f"Elapsed time: {end_time - start_time:.4f} seconds")
    print("Résultats :", results)
