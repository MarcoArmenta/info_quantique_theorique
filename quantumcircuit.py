class QuantumCircuit:

    def __init__(self, circuit):
        if type(circuit[0]) is list:
            circuit = circuit[0]  # Sélectionne le premier circuit si nécessaire
        self.n_qubits = circuit[0]
        self.stabilisateur = []
        for i in range(self.n_qubits):
            V_x = [0] * self.n_qubits  # chaîne de 0 pour les X
            V_z = [0] * self.n_qubits  # chaîne de 0 pour les Z
            V_z[i] = 1  # initialisation dans |0> pour chaque qubit dans Z
            s = 0  # Pas d'inversion de signe initialement
            self.stabilisateur.append({'V_x': V_x, 'V_z': V_z, 's': s})

    def application_hadamard(self, q):
        for ligne in self.stabilisateur:
            # Échanger V_x et V_z
            valeur_V_x_temporaire = ligne['V_x'][q]
            ligne['V_x'][q] = ligne['V_z'][q]
            ligne['V_z'][q] = valeur_V_x_temporaire
        #print(f"Après Hadamard sur {q}: {self.stabilisateur}")

    def application_de_S(self, q):
        for ligne in self.stabilisateur:
            # Ajouter V_x à V_z modulo 2
            ligne['V_z'][q] = (ligne['V_z'][q] + ligne['V_x'][q]) % 2
        #print(f"Après S sur {q}: {self.stabilisateur}")


    def CX(self, controle, cible):
        for ligne in self.stabilisateur:
            # Ajouter V_z[cible] à V_z[controle] modulo 2
            ligne['V_z'][controle] = (ligne['V_z'][controle] + ligne['V_z'][cible]) % 2
            # Ajouter V_x[controle] à V_x[cible] modulo 2
            ligne['V_x'][cible] = (ligne['V_x'][cible] + ligne['V_x'][controle]) % 2
        #print(f"Après CX entre {controle} et {cible}: {self.stabilisateur}")

    def application_de_pauli(self, q, pauli):
        for ligne in self.stabilisateur:
            if pauli == 'X':
                # Inversion de signe si Z est présent à l'emplacement q
                if ligne['V_z'][q] == 1 :
                    ligne['s'] = -ligne['s']
            elif pauli == 'Z':
                # Inversion de signe si X est présent à l'emplacement q
                if ligne['V_x'][q] == 1 :
                    ligne['s'] = -ligne['s']
            elif pauli == 'Y':
                if ligne['V_x'][q] == 1 and ligne['V_z'][q] == 1 :
                    ligne['s'] = -ligne['s']
                elif ligne['V_x'][q] == 1 and ligne['V_z'][q] == 0 :  
                    ligne['s'] = -ligne['s']
                elif ligne['V_x'][q] == 0 and ligne['V_z'][q] == 1 :  
                    ligne['s'] = -ligne['s']  
        #print(f"Après application de Pauli {pauli} sur {q}: {self.stabilisateur}")
