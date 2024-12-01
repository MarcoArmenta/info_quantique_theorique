"""
Auteur: Jérémie Boudreault
"""


class QuantumCircuit:
    """
    Classe qui prend en entrée un loaded json et qui prend
    en charge les gate H, S, CX et Paulis (X,Y,Z). L'objet
    QuantumCircuit conserve la structure du loaded json,
    c'est-à-dire [nb_qubits, observables, valeurs propres, portes logiques].
    """
    def __init__(self, l):
        """
        :param l: loaded json file
        """
        self.qc = l
        return

