# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 19:43:06 2024

@author: iphone
"""

import numpy as np
from multiprocessing import Pool

class GKSimulator:
    def __init__(self):
        pass

    def process_circuit(self, circuit, cq): # Les commentaires sont genere par GPT-4o
        """
        Process a single circuit configuration
        
        Args:
            circuit: The circuit object
            cq: Circuit configuration index
        
        Returns:
            dict: Measurement results for this circuit configuration
        """
        
        stab = [["i" for j in range(circuit.num_qubits[cq])] for i in range(circuit.num_qubits[cq])]  #generer par chatgpt
        phase = [1 for j in range(circuit.num_qubits[cq])]  #generer par chatgpt
        for i in range(circuit.num_qubits[cq]):
            stab[i][i] = "z"
        
        # Simulate circuit gates
        for gate_info in circuit.gates[cq]:         # une partie de cette boucle generer par AI
            for j in range(len(list(gate_info.keys()))):
                gate_type = list(gate_info.keys())[j]                    #generer par claud.ai
                gate_targets = gate_info[gate_type]                    #generer par claud.ai
                if gate_type == 'h':                    #generer par claud.ai
                    stab, phase = circuit.apply_hadamard(stab, gate_targets, phase)                    #generer par claud.ai
                elif gate_type == 's':                    #generer par claud.ai
                    stab, phase = circuit.apply_s(stab, gate_targets, phase)                    #generer par claud.ai
                elif gate_type == 'cx':                    #generer par claud.ai
                    stab, phase = circuit.apply_cx(stab, list(gate_targets), phase)                    #generer par claud.ai
                elif gate_type in ['x', 'y', 'z']:                    #generer par claud.ai
                    stab, phase = circuit.apply_pauli(gate_type, stab, gate_targets, phase)                    #generer par claud.ai                    #generer par claud.ai
        
        # Measurement logic
        obs_str = circuit.observable[cq]
        obs = list(obs_str)
        
        plus = False
        count = -1
        ind = 0
        for stab_ in stab:
            count = count + 1    
            if obs == stab_:
                plus = True
                ind = count
                break
            
        if plus == True and phase[ind] == 1:
            prob = {"+": 1.0, "-": 0.0}
        elif plus == True and phase[ind] == -1:
            prob = {"+": 0.0, "-": 1.0}
        else:
            prob = {"+": 0.5, "-": 0.5}
        
        resultat = dict()
        for vp in circuit.eigenvalues[cq]:
            if vp == '+':
                resultat.update({'+': prob['+']})
                #resultat.update({'+': 0.5})
            elif vp == '-':
                resultat.update({'-': prob['-']})
                #resultat.update({'-': 0.5})
        
        return resultat

    def run(self, circuit): # cette methode generer par GPT-4o et les commentaires aussi
        """
        Run circuit simulation using multiprocessing
    
        Args:
            circuit: The circuit to simulate
    
        Returns:
            list: Results for each circuit configuration
            """
        num_cores = 8
        with Pool(processes=num_cores) as pool:  
            # Map the process_circuit function across the range of num_qubits
            results = pool.starmap(self.process_circuit, [(circuit, cq) for cq in range(len(circuit.num_qubits))])
        return results