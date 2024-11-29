"""
Fichier contenant la classe qui permet de formaliser les observables fournient pour chacun des
circuits sous la forme de `PauliObservable`.
"""



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
