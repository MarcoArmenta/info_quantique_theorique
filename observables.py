class PauliObservable:
    def __init__(self, chaine_pauli):
        self.chaine_pauli = chaine_pauli
        self.n_qubits = len(chaine_pauli)

    def convertir_en_px_pz(self):
        P_x = [0] * self.n_qubits
        P_z = [0] * self.n_qubits
        for i, pauli in enumerate(self.chaine_pauli):
            if pauli == 'X':
                P_x[i] = 1
            elif pauli == 'Z':
                P_z[i] = 1
            elif pauli == 'Y':
                P_x[i], P_z[i] = 1, 1
        return {'P_x': P_x, 'P_z': P_z}

    def appliquer_observable(self, circuit):
        for q, pauli in enumerate(self.chaine_pauli):
            if pauli != 'I':
                circuit.appliquer_pauli(q, pauli)
