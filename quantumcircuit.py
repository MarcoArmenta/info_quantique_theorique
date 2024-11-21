import numpy as np



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
        pass