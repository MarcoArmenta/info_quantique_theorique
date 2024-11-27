import json
import numpy as np

from observables import PauliObservable



class QuantumCircuit:
    """
    Classe qui prend en charge les portes H, S, CX, et n'importe quelle autre porte Pauli.
    """
    def __init__(self, l: list):
        """
        Description
        -----------
        Initialiser la class.

        Paramètres
        ----------
        l: list
            Une liste contenant dans l'ordre: le nombre de qubits, l'observable à mesurer, une
            liste avec les valeurs propres pour lesquelles calculer les probabilités de mesure, et
            des dictionnaires avec les portes à appliquer.
        """
        self.l = l
        for circ in self.l:
            circ[1] = PauliObservable(circ[1])
            # self._translate_eig_vals_to_bool(circ[2])

    # def _translate_eig_vals_to_bool(self, eig_vals: list):
    #     """
    #     Traduire les valeurs propres en valeurs booléennes pour une représentation plus légères des
    #     informations.
    #     """
    #     zeros = np.zeros(len(eig_vals), dtype=bool)
    #     for eig_val_idx, eig_val in enumerate(eig_vals):
    #         if eig_val == "-":
    #             zeros[eig_val_idx] = True
    #     circ[2] = zeros


if __name__ == "__main__":
    with open('dummy_circuits.json', 'r') as file:
        l = json.load(file)
    print(l)
    q = QuantumCircuit(l)
    print(q.l)