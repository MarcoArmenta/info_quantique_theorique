import numpy as np
from multiprocessing.pool import Pool

from observables import PauliObservable
from quantumcircuit import QuantumCircuit



class GKSimulator:
    """
    Classe qui dispose d'une méthode pour mesurer une observable de Pauli donnée.
    """
    def __init__(self):
        """
        Initialiser la classe `GKSimulator`.
        """
        pass

    def _single_circ_run(self, circ: list):
        """
        Extraire les mesures des probabilités des valeurs propres d'un circuit.
        """
        self.num_qubits = circ[0]
        observable = circ[1]
        sing_values = circ[2]
        blocks = circ[3:]
        dim = 2 * self.num_qubits
        # n premières lignes: dé-stabilisateurs
        # n dernières lignes: stabilisateurs
        self.tableau = np.eye(dim, dim+1, dtype=bool)
        self.apply_gate_fns_dict = {
            "x":  self._apply_x_gate,
            "y":  self._apply_y_gate,
            "z":  self._apply_z_gate,
            "h":  self._apply_h_gate,
            "cx": self._apply_cx_gate,
            "s":  self._apply_s_gate,
        }
        # Updater le tableau
        for block in blocks:
            self._update_tableau(block)
        # Extrai les mesures
        result = self._measure_from_updated_tableau(observable, sing_values)
        return result

    def _apply_x_gate(self, qubit_ids: list):
        """
        Évoluer le tableau lorsqu'on applique la porte X sur les qubit `qubits_ids`.
        """
        cols = [idx + self.num_qubits for idx in qubit_ids] + [-1]
        self.tableau[:,-1] = np.logical_xor.reduce(self.tableau[:, cols], axis=1)

    def _apply_y_gate(self, qubit_ids: list):
        """
        Évoluer le tableau lorsqu'on applique la porte Y sur les qubit `qubits_ids`.
        """
        cols = qubit_ids + [idx + self.num_qubits for idx in qubit_ids] + [-1]
        self.tableau[:,-1] = np.logical_xor.reduce(self.tableau[:, cols], axis=1)

    def _apply_z_gate(self, qubit_ids: list):
        """
        Évoluer le tableau lorsqu'on applique la porte Z sur les qubit `qubits_ids`.
        """
        cols = qubit_ids + [-1]
        self.tableau[:,-1] = np.logical_xor.reduce(self.tableau[:, cols], axis=1)

    def _apply_h_gate(self, qubit_ids: list):
        """
        Évoluer le tableau lorsqu'on applique la porte H sur les qubit `qubits_ids`.
        """
        x_cols = qubit_ids
        z_cols = [idx + self.num_qubits for idx in qubit_ids]
        self.tableau[:,-1] = self.tableau[:,-1] ^ np.logical_xor.reduce((self.tableau[:,x_cols] & self.tableau[:,z_cols]), axis=1)
        self.tableau[:, x_cols+z_cols] = self.tableau[:, z_cols+x_cols]

    def _apply_cx_gate(self, qubit_ids: list):
        """
        Évoluer le tableau lorsqu'on applique la porte CNOT sur les qubit `qubits_ids`.
        """
        x_ctrl_qubits, x_trgt_qubits = list(zip(*qubit_ids))
        z_ctrl_qubits, z_trgt_qubits = [idx + self.num_qubits for idx in x_ctrl_qubits], [idx + self.num_qubits for idx in x_trgt_qubits]
        self.tableau[:,-1] = self.tableau[:,-1] ^ np.logical_xor.reduce(
            (
                self.tableau[:,x_ctrl_qubits] & self.tableau[:,z_trgt_qubits]
            ) & (
                self.tableau[:,x_trgt_qubits] ^ self.tableau[:,z_ctrl_qubits] ^ True
            ),
            axis=1,
        )
        self.tableau[:,x_trgt_qubits] ^= self.tableau[:,x_ctrl_qubits]
        self.tableau[:,z_ctrl_qubits] ^= self.tableau[:,z_trgt_qubits]

    def _apply_s_gate(self, qubit_ids: list):
        """
        Évoluer le tableau lorsqu'on applique la porte S sur les qubit `qubits_ids`.
        """
        x_cols = qubit_ids
        z_cols = [idx + self.num_qubits for idx in qubit_ids]
        self.tableau[:,-1] = self.tableau[:,-1] ^ np.logical_xor.reduce((self.tableau[:,x_cols] & self.tableau[:,z_cols]), axis=1)
        self.tableau[:, z_cols] ^= self.tableau[:, x_cols]

    def _update_tableau(self, block: dict):
        """
        Évoluer le tableau après l'application d'un bloc de portes `block` dans le circuit.
        """
        for gate, qubit_ids in block.items():
            self.apply_gate_fns_dict[gate](qubit_ids=qubit_ids)

    def _measure_from_updated_tableau(self, observable: PauliObservable, sing_values: list):
        """
        Déterminer la mesure des valeurs propres "+" et "-" à la fin du circuit selon
        l'observable donnée.
        """
        measure = {sing_value: None for sing_value in sing_values}
        obs = observable.obs_bool
        x_and_z_swapped_obs = np.roll(obs, self.num_qubits)
        stabs = self.tableau[self.num_qubits:, :-1]
        symplectic_products = np.logical_xor.reduce(stabs & x_and_z_swapped_obs, axis=1)
        if not np.any(symplectic_products):
            r_values = self.tableau[:,-1]
            tableau_T_inv = self._find_inverse_of_bool_matrix()
            coeffs = np.logical_xor.reduce(tableau_T_inv & obs, axis=1)
            # print(coeffs)
            # coeffs = np.linalg.solve(self.tableau[:,:-1].T, obs).astype(bool)
            if np.logical_xor.reduce(r_values & coeffs):
                prob = 0
            else:
                prob = 1
            measure = {"+": prob, "-": (prob+1)%2}
        else:
            prob = 1/2
            measure = {"+": prob, "-": prob}
        return measure

    def _find_inverse_of_bool_matrix(self):
        """
        Appliquer l'élimination gaussienne sur le tableau complètement évolué (une matrice booléenne) dans GF(2).
        * La multiplication est équivalente à `&` et l'addition à `^` dans GF(2).

        Retourne
        --------
        np.ndarray:
            La matrice booléenne inverse du tableau.
        """
        # Augment the tableau boolean matrix (without the `r` column) with the identity ([A | I])
        matrix = np.hstack((self.tableau[:,:-1].T, np.eye(2*self.num_qubits, dtype=bool)))

        for col in range(2*self.num_qubits):
            # Find pivot row with a True in the current column
            pivot_row = None
            for row in range(col, 2*self.num_qubits):
                if matrix[row, col]:
                    pivot_row = row
                    break
            # If no pivot is in this column, move to the next column
            if pivot_row is None:
                continue

            # Switch the pivot row to the current row
            if pivot_row != col:
                matrix[[col, pivot_row]] = matrix[[pivot_row, col]]

            # Eliminate other entries in the current column
            for row in range(2*self.num_qubits):
                if row != col and matrix[row, col]:
                    matrix[row] ^= matrix[col]  # Row reduction using XOR

        return matrix[:,2*self.num_qubits:] # extraire A^-1 de [I | A^-1]

    def run(self, q: QuantumCircuit):
        """
        Mesurer une observable de Pauli donnée.

        Paramètre
        ---------
        q: QuantumCircuit
            Une liste de circuits quantiques générés par la classe `QuantumCircuit`.
        """
        max_cores = 8
        with Pool(processes=max_cores) as pool:
            results = pool.map(self._single_circ_run, q.l)
        # results = []
        # for circ in q.l:
        #     result = self._single_circ_run(circ)
        #     results.append(result)
        print(results)
        return results
