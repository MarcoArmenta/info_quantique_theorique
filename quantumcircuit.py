class QuantumCircuit:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.stabilizers = ['I'] * num_qubits

    def apply_hadamard(self, target_qubit):
        pass

    def apply_s(self, target_qubit):
        pass

    def apply_cx(self, control_qubit, target_qubit):
        pass

    def apply_pauli(self, pauli_type, target_qubit):
        if pauli_type not in ('X', 'Y', 'Z'):
            raise ValueError("Type de porte Pauli invalide. Utilisez 'X', 'Y' ou 'Z'.")
        pass
