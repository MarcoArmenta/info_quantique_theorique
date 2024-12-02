# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 19:43:06 2024

@author: iphone
"""

import numpy as np

class GKSimulator:
    def __init__(self):
        pass

    def run(self, circuit):
        results = []
        for cq in range(len(circuit.num_qubits)): # repeter la boucle pour chaque circuit
            Id = np.eye(2, dtype=int)
            stab = [[Id for j in range(circuit.num_qubits[cq])] for i in range(circuit.num_qubits[cq])] #generer par chatgpt
            for i in range(circuit.num_qubits[cq]):
                stab[i][i] = circuit.pauli_gate('z')
            
            
            
            # une partie de cette boucle generer par AI
            for gate_info in circuit.gates[cq]:
            #gate_info est un dictionnaire contient les portes logiques
                for j in range(len(list(gate_info.keys()))):
                    gate_type = list(gate_info.keys())[j]                    #generer par claud.ai
                    gate_targets = gate_info[gate_type]                   #generer par claud.ai
                    if gate_type == 'h':                   #generer par claud.ai
                        
                        stab = circuit.apply_hadamard(stab, gate_targets)                   #generer par claud.ai
                    elif gate_type == 's':                   #generer par claud.ai
                        
                        stab = circuit.apply_s(stab, gate_targets)                   #generer par claud.ai
                    elif gate_type == 'cx':                   #generer par claud.ai
                        
                        stab = circuit.apply_cx(stab, list(gate_targets))                   #generer par claud.ai
                    elif gate_type in ['x', 'y', 'z']:                   #generer par claud.ai
                        
                        stab = circuit.apply_pauli(gate_type, stab, gate_targets)                   #generer par claud.ai
            
            # implementer la mesure:
            
            obs_str = circuit.observable[cq]
            obs = list(obs_str)
            obser = []
            index = []
            ind = 0
            for p in obs:
                if p == 'i':
                    obser.append(np.eye(2, dtype=int))
                elif p == 'z':
                    obser.append(circuit.pauli_gate('z'))
                    index.append(ind)
                elif p == 'x':
                    obser.append(circuit.pauli_gate('x'))
                    index.append(ind)
                    
                ind = ind + 1
            
            obs_tens = 1
            for i in index:
                obs_tens = np.kron(obs_tens, obser[i])
                
            commute = True
            for stab_ in stab:
                stab_tens = 1
                for i in index:
                    stab_tens = np.kron(stab_tens, stab_[i])
                
                if not np.array_equal(np.dot(stab_tens, obs_tens), np.dot(obs_tens, stab_tens)):
                    commute = False
                    break
    
            if commute == False:
                prob = {"+": 0.5, "-": 0.5}
            elif commute == True:
                plus = False
                obs_tens = 1
                for i in range(len(obser)):
                    obs_tens = np.kron(obs_tens, obser[i])
                for stab_ in stab:
                    stab_tens = 1
                    for i in range(len(obser)):
                        stab_tens = np.kron(stab_tens, stab_[i])
                    if np.array_equal(obs_tens, stab_tens):
                        plus = True
                        break
                if plus == True:
                    prob = {"+": 1, "-": 0}
                elif plus == False:
                    prob = {"+": 0, "-": 1}
            resultat = dict()
            for vp in circuit.eigenvalues[cq]:
                if vp == '+':
                    resultat.update({'+': prob['+']})
                elif vp == '-':
                    resultat.update({'-': prob['-']})
            results.append(resultat)
                
        
            
        # Ajouter les résultats à la liste
        return results