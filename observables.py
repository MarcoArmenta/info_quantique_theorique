"""
Fichier contenant la classe permettant de traduire les observables sous la forme de `str` ou de
vecteurs booléens.
"""



import numpy as np



class PauliObservable:
    """
    Class permettant de représenter une observable de Pauli.
    """
    def __init__(self, obs: str):
        """
        Représenter une observable de Pauli donnée.

        Paramètre
        ---------
        obs: str
            Une observable de Pauli.
        """
        self.obs = obs.lower()
        self.str_to_bool(obs)

    def str_to_bool(self, obs: str):
        """
        Traduire les observables en valeurs booléennes pour la représentation en tableau.

        Paramètre
        ---------
        obs: str
            L'observable à traduire sous la forme d'un vecteur booléen.
        """
        # Initialize the tableau with all False
        num_qubits = len(obs)
        self.obs_bool = np.zeros(2*num_qubits, dtype=bool)

        # Parse the observable
        for idx, str_obs in enumerate(self.obs):
            if str_obs == 'x':  # X operator
                self.obs_bool[idx] = True
            elif str_obs == 'z':  # Z operator
                self.obs_bool[idx+num_qubits] = True
            elif str_obs == 'y': # Y operator
                self.obs_bool[idx] = True
                self.obs_bool[idx+num_qubits] = True
