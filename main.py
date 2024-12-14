import json
import psutil
import os
import time
from quantumcircuit import QuantumCircuit
from simulator import GKSimulator

def get_memory_usage():
    """
    Get the current memory usage of the process.

    :return: Memory usage in MB
    """
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB

if __name__ == "__main__":
    # Load circuits data from JSON file
    with open("dummy_circuits.json", "r") as file:
        circuits_data = json.load(file)

    results = []
    mem_before = get_memory_usage()  # Memory before execution
    start_time = time.perf_counter()  # Start time for performance measurement

    simulator = GKSimulator()  # Initialize the simulator once

    for circuit_data in circuits_data:
        if len(circuit_data) != 4:
            print("Error: Incorrect data format for circuit.")
            continue  # Skip incorrect format data

        # Create a QuantumCircuit instance with the data
        circuit = QuantumCircuit(circuit_data)
        
        # Execute the circuit
        result = simulator.executer(circuit)  # Correct method call
        results.append(result)

    mem_after = get_memory_usage()  # Memory after execution
    end_time = time.perf_counter()  # End time for performance measurement

    # Print results and performance metrics
    print(f"Memory usage: {mem_after - mem_before:.2f} MB")
    print(f"Elapsed time: {end_time - start_time:.4f} seconds")
    print("Results:", results)
