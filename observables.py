"""
Module to store Pauli observables.
"""


class PauliObservable:
    """
    Class to store a Pauli observable.

    Attributes:
    ----------
    num_qubits : int
        Number of qubits in the Pauli string.
    i_qubits : list
        List of qubits with identity operator.
    x_qubits : list
        List of qubits with Pauli-X operator.
    y_qubits : list
        List of qubits with Pauli-Y operator.
    pauli_string : str
        Pauli string.
    """

    def __init__(self, pauli_string):

        i_qubits = []
        x_qubits = []
        y_qubits = []
        z_qubits = []
        for i, char in enumerate(pauli_string):
            if char == "i":
                i_qubits.append(i)
            elif char == "x":
                x_qubits.append(i)
            elif char == "y":
                y_qubits.append(i)
            elif char == "z":
                z_qubits.append(i)

        self.num_qubits = len(pauli_string)
        self.i_qubits = i_qubits
        self.x_qubits = x_qubits
        self.y_qubits = y_qubits
        self.z_qubits = z_qubits
        self.pauli_string = pauli_string
