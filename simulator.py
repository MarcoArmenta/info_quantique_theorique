# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:54:34 2024

@author: lenovo
"""
from concurrent.futures import ProcessPoolExecutor
from observables import PauliObservable


class GKSimulator:
    def __init__(self):
        pass

    def run(self, quantum_circuit):
        
        results = []
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self._simulate_circuit, circuit) for circuit in quantum_circuit.circuits]
            for future in futures:
                results.append(future.result())
        return results

    def _simulate_circuit(self, circuit):
     
        for gate_dict in circuit["gates"]:
            for gate, targets in gate_dict.items():
                for target in targets:
                    circuit["quantum_circuit"].apply_gate(circuit, gate, target)
        observable = PauliObservable(circuit["observable"])
        return observable.measure(circuit["stabilizer_table"])
