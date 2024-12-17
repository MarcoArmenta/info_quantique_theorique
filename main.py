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
    return process.memory_info().rss / (1024 * 1024)  

def main():
    
    with open("dummy_circuits.json", "r") as file:
        circuits_to_simulate = json.load(file)

  
    results = []

   
    mem_before = get_memory_usage()
    start_time = time.perf_counter()

    
    for idx, circuit_data in enumerate(circuits_to_simulate):
        print(f"Simulation du circuit {idx + 1}...")

       
        n_qubits = circuit_data[0]  
        circuit = QuantumCircuit(n_qubits)

      
        for gate_set in circuit_data[3:]:  
            for gate, targets in gate_set.items():
                for target in (targets if isinstance(targets, list) else [targets]):
                    if isinstance(target, list):  
                        circuit.ajouter_porte(gate, *target)
                    else:
                        circuit.ajouter_porte(gate, target)

        
        simulator = GKSimulator()

        
        result = simulator.executer(circuit)
        results.append(result)

   
    end_time = time.perf_counter()
    mem_after = get_memory_usage()

    
    print(f"Memory usage: {mem_after - mem_before:.2f} MB")
    print(f"Elapsed time: {end_time - start_time:.4f} seconds")
    print("Résultats des simulations :")
    for idx, res in enumerate(results):
        print(f"Circuit {idx + 1}: {res}")

if __name__ == "__main__":
    main()
