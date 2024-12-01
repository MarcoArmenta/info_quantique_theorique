import json
import numpy as np
from observables import PauliObservable

with open('dummy_circuits.json', 'r') as file:
    l = json.load(file)


table = np.arange(0,36,1).reshape([6,6])
print(table)
n = int(table.shape[0] / 2)
target = 0
print(table[n:, -1])
table[n:, -1] = (table[n:, -1] + table[n:, target - 1] * table[n:,target - 1 + n]) % 2
print(table)

n_qubit, Os, eig_vals, gates_dict = l[0]


# loaded json = list(int #qubits, 'pauli string of observables',
#                 ['list of eigenvalue string'], {'dict of gates and' : [which qubits to apply them to]})

# zi est z tensor identity