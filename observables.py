class PauliObservable:
    def __init__(self, chaine_pauli):
        self.chaine_pauli = chaine_pauli
        self.n_qubits = len(chaine_pauli)

    def convertir_en_px_pz(self): # Comme on extrait nos observable du fichier json, on les réecrit sous forme vectorielle
        P_x = [0] * self.n_qubits
        P_z = [0] * self.n_qubits
        for i, pauli in enumerate(self.chaine_pauli):
            if pauli == 'x':
                P_x[i] = 1
            elif pauli == 'z':
                P_z[i] = 1
            elif pauli == 'y':
                P_x[i] = 1
                P_z[i] = 1
        return {'P_x': P_x, 'P_z': P_z}

    def appliquer(self, circuit): # on applique l'observable de pauli au circuit donné.
        for q, pauli in enumerate(self.chaine_pauli):
            if pauli != 'I':  # Ignore 'I' (identité)
                circuit.application_de_pauli(q, pauli)
