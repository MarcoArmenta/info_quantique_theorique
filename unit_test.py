from simulator import *
from observables import PauliObservables
from quantumcircuit import QuantumCircuit
import numpy as np
from qiskit.quantum_info import Statevector, StabilizerState, Pauli
from qiskit import QuantumCircuit as qct


def qiskit_circuit_run(circuit_data):
    """
    Build a Qiskit QuantumCircuit based on the input circuit data.
    Args:
        circuit_data (list): A list containing the circuit details in the form:
                             [n_qbits, pauli, signs, gates_dict]
    Returns:
        QuantumCircuit: The constructed Qiskit circuit.
    """
    n_qbits = circuit_data[0]
    gates_dict = circuit_data[3:]  # The dictionary of gates and their targets
    pauli_op = str.upper(circuit_data[1])

    # Initialize the Qiskit quantum circuit
    qc = qct(n_qbits)

    # Iterate through the gates and apply them to the circuit
    for gate_list in gates_dict:
        for gate, targets in gate_list.items():
            for target in targets:
                if isinstance(target, list):  # Handle 2-qubit gates (e.g., CX)
                    if gate == "cx":
                        qc.cx(target[0], target[1])
                    else:
                        raise ValueError(f"Unsupported 2-qubit gate: {gate}")
                else:  # Handle single-qubit gates
                    if gate == "x":
                        qc.x(target)
                    elif gate == "y":
                        qc.y(target)
                    elif gate == "z":
                        qc.z(target)
                    elif gate == "h":
                        qc.h(target)
                    elif gate == "s":
                        qc.s(target)
                    else:
                        raise ValueError(f"Unsupported gate: {gate}")
                    
    
    results = StabilizerState(qc)
    return results


#I used chat gpt to write the random list of 20 circuits
circuits = [
    [4, "xzzi", ["+", "-"], {"x": [0, 2], "cx": [[1, 2]], "h": [3], "z": [2]}],
    [3, "zii", ["+"], {"x": [0], "y": [1], "s": [2]}],
    [6, "xzzzix", ["-", "+"], {"z": [4], "cx": [[2, 5]], "h": [3], "y": [1], "x": [0]}],
    [2, "ix", ["+"], {"h": [1], "cx": [[0, 1]]}],
    [5, "zxzzx", ["-", "+"], {"s": [0], "y": [2], "x": [3], "cx": [[1, 4]]}],
    [3, "xzx", ["-"], {"z": [1], "h": [2], "y": [0]}],
    [6, "xxziix", ["+", "-"], {"cx": [[0, 2]], "z": [5], "h": [3], "s": [4]}],
    [4, "ixxz", ["+"], {"x": [1], "y": [3], "z": [0]}],
    [3, "xxx", ["-", "+"], {"h": [1], "x": [0], "cx": [[1, 2]]}],
    [5, "zizii", ["+"], {"z": [0], "h": [4], "cx": [[3, 2]]}],
    [6, "xxxxzi", ["-", "+"], {"x": [2], "s": [1], "y": [3], "cx": [[0, 4]]}],
    [4, "zxxz", ["+"], {"y": [0], "x": [1], "h": [3]}],
    [2, "yx", ["-"], {"z": [0], "cx": [[1, 0]]}],
    [3, "iiz", ["+"], {"h": [2], "x": [0], "s": [1]}],
    [5, "zxzzx", ["-", "+"], {"s": [3], "z": [4], "y": [1], "cx": [[0, 2]]}],
    [6, "izzxzz", ["-"], {"x": [2], "cx": [[4, 5]], "y": [0], "h": [3]}],
    [4, "xxzz", ["+", "-"], {"h": [3], "y": [1], "z": [2]}],
    [3, "zxz", ["+"], {"s": [0], "h": [2], "cx": [[1, 0]]}],
    [6, "xzxzzz", ["-"], {"z": [4], "y": [2], "x": [3], "cx": [[0, 5]]}],
    [2, "ix", ["+"], {"x": [1], "h": [0]}],
]

r = []
for circuit in circuits:
    print(circuit)
    q = QuantumCircuit(circuit)
    s = GKSimulator(q)
    r.append(s.run(q))
    print(q.get_stabilizers())
print(r)

qiskit_results = []

for circuit in circuits:
    qiskit_results.append(qiskit_circuit_run(circuit))
print(qiskit_results)