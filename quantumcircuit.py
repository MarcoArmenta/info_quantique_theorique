# quantumcircuit
import numpy as np
import json
import psutil
import os
import time

from observables import PauliObservable

class QuantumCircuit:
    def __init__(self, jsf):
        
        self.struct = [self._transform(circ) for circ in jsf]

    # function that deal data manipulation to prepare for simulation
    def _transform(self, circ):
        output_list = [
                        circ[0],
                        PauliObservable(circ[1], circ[0]),
                        self._meas_str_2_vec(circ[2]),
                        [circ[index+3] for index in range(len(circ)-3)]
                       ]
        return output_list
    
    # function to map observable eigenvalues as string to bool eigenvalues
    def _meas_str_2_vec(self, eig_list_str):
        return [meas == "-" for meas in eig_list_str]


if __name__ == "__main__":
    with open('dummy_circuits.json', 'r') as file:
        l = json.load(file)
    
    q = QuantumCircuit(l)
