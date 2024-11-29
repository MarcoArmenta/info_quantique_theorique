"""
Fichier permettant de tester le simulateur `GKSimulator` afin de vérifier si elle donne les bons
résultats de mesure pour des circuits quantiques connus.
"""



import sys, os
# Make it possible for `pytest` to import classes from files in this folder
sys.path.append(os.path.realpath(os.path.dirname(__file__)))

import pytest
import numpy as np

from quantumcircuit import QuantumCircuit
from simulator import GKSimulator



def test_no_circuit():
    """Test de la simulation lorsqu'on a un circuit vide."""
    l = [
        [0, "", ["+", "-"], {}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r == [{"+": None, "-": None}]

def test_identity_circuit():
    """Test de la simulation lorsqu'on n'applique rien sur un circuit d'un seul qubit."""
    l = [
        [1, "z", ["+", "-"], {}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r == [{"+": 1, "-": 0}]

def test_x_circuit():
    """Test de la simulation lorsqu'on applique une porte X sur un circuit d'un seul qubit."""
    l = [
        [1, "z", ["+", "-"], {"x": [0]}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r == [{"+": 0, "-": 1}]

def test_y_circuit():
    """Test de la simulation lorsqu'on applique une porte Y sur un circuit d'un seul qubit."""
    l = [
        [1, "z", ["+", "-"], {"y": [0]}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r == [{"+": 0, "-": 1}]

def test_z_circuit():
    """Test de la simulation lorsqu'on applique une porte Z sur un circuit d'un seul qubit."""
    l = [
        [1, "z", ["+", "-"], {"z": [0]}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    print(r)
    assert r == [{"+": 1, "-": 0}]

def test_h_circuit():
    """Test de la simulation lorsqu'on applique une porte H sur un circuit d'un seul qubit."""
    l = [
        [1, "z", ["+", "-"], {"h": [0]}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    print(r)
    assert r == [{"+": 0.5, "-": 0.5}]

def test_cx_circuit():
    """Test de la simulation lorsqu'on applique une porte CNOT sur un circuit de deux qubits."""
    l = [
        [2, "zz", ["+", "-"], {"cx": [[0,1]]}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    print(r)
    assert r == [{"+": 1, "-": 0}]

def test_s_circuit():
    """Test de la simulation lorsqu'on applique une porte S sur un circuit d'un seul qubit."""
    l = [
        [1, "z", ["+", "-"], {"s": [0]}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r == [{"+": 1, "-": 0}]

@pytest.mark.parametrize("obs, result",
    [
        ("zi", [{"+": 0.5, "-": 0.5}]),
        ("iz", [{"+": 0.5, "-": 0.5}]),
        ("zz", [{"+": 1, "-": 0}]),
    ]
)
def test_bell_pair_circuit0(obs: str, result: list):
    """Tests de la simulation d'un circuit générant une paire de Bell pour 3 différentes
    observables."""
    l = [
        [2, obs, ["+", "-"], {"h": [0], "cx": [[0,1]]}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r == result

@pytest.mark.parametrize("obs, result",
    [
        ("zi", [{"+": 0.5, "-": 0.5}]),
        ("iz", [{"+": 0.5, "-": 0.5}]),
        ("zz", [{"+": 0, "-": 1}]),
    ]
)
def test_bell_pair_circuit1(obs: str, result: list):
    """Tests de la simulation d'un circuit générant une paire de Bell pour 3 différentes
    observables."""
    l = [
        [2, obs, ["+", "-"], {"h": [0], "cx": [[0,1]], "x": [0]}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r == result

@pytest.mark.parametrize("obs, result",
    [
        ("zi", [{"+": 0.5, "-": 0.5}]),
        ("iz", [{"+": 0.5, "-": 0.5}]),
        ("zz", [{"+": 1, "-": 0}]),
    ]
)
def test_bell_pair_circuit2(obs: str, result: list):
    """Tests de la simulation d'un circuit générant une paire de Bell pour 3 différentes
    observables."""
    l = [
        [2, obs, ["+", "-"], {"h": [0], "z": [0], "cx": [[0,1]]}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r == result

@pytest.mark.parametrize("obs, result",
    [
        ("zi", [{"+": 0.5, "-": 0.5}]),
        ("iz", [{"+": 0.5, "-": 0.5}]),
        ("zz", [{"+": 0, "-": 1}]),
    ]
)
def test_bell_pair_circuit3(obs: str, result: list):
    """Tests de la simulation d'un circuit générant une paire de Bell pour 3 différentes
    observables."""
    l = [
        [2, obs, ["+", "-"], {"h": [0], "z": [0], "cx": [[0,1]], "x": [0]}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r == result

@pytest.mark.parametrize("obs, result",
    [
        ("zzz", [{"+": 0.5, "-": 0.5}]),
        ("zzi", [{"+": 1, "-": 0}]),
        ("ziz", [{"+": 1, "-": 0}]),
        ("izz", [{"+": 1, "-": 0}]),
        ("zii", [{"+": 0.5, "-": 0.5}]),
        ("izi", [{"+": 0.5, "-": 0.5}]),
        ("iiz", [{"+": 0.5, "-": 0.5}]),
        
    ]
)
def test_ghz_circuit(obs: str, result: list):
    """Tests de la simulation d'un circuit générant un état GHZ pour 7 différentes
    observables."""
    l = [
        [3, obs, ["+", "-"], {"h": [0], "cx": [[0,1]]},{"cx": [[1,2]]}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r == result

@pytest.mark.parametrize("obs, result",
    [
        ("zz", [{"+": 0.5, "-": 0.5}]),
        ("iz", [{"+": 0.5, "-": 0.5}]),
        ("zi", [{"+": 0.5, "-": 0.5}]),
    ]
)
def test_phase_kickback(obs: str, result: list):
    """Tests de la simulation d'un circuit de "phase-kickback" avec un CNOT pour 3 différentes
    observables."""
    l = [
        [2, obs, ["+", "-"],{"h": [0], "cx": [[0, 1]]}, {"h": [0]}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r == result

@pytest.mark.parametrize("num_qubits", 
    [
        2,3,4,5,6,7,8,9
    ]
)
def test_all_hadamard_circuit(num_qubits: int):
    """Test de la simulation lorsqu'on applique une porte H sur 4 qubits."""
    l = [
        [num_qubits, "z"*num_qubits, ["-"], {"h": list(range(num_qubits))}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r == [{"-": 0.5}]

def test_HXH_equivalent_to_Z_circuit():
    """Test de l'équivalence entre HXH et Z dans un circuit à 3 qubits."""
    nb_qubits = 3
    obs = "zzz"
    all_qubits = list(range(nb_qubits))
    l = [
        [nb_qubits, obs, ["+","-"], {"h": all_qubits, "x": all_qubits}, {"h": all_qubits}],
        [nb_qubits, obs, ["+","-"], {"z": all_qubits}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r[0] == r[1]

def test_HZH_equivalent_to_X_circuit():
    """Test de l'équivalence entre HZH et X dans un circuit à 3 qubits."""
    nb_qubits = 3
    obs = "zzz"
    all_qubits = list(range(nb_qubits))
    l = [
        [nb_qubits, obs, ["+","-"], {"h": all_qubits, "z": all_qubits}, {"h": all_qubits}],
        [nb_qubits, obs, ["+","-"], {"x": all_qubits}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r[0] == r[1]

def test_XY_equivalent_to_Z():
    """Test de l'équivalence entre XY et Z dans un circuit à 3 qubits."""
    nb_qubits = 3
    obs = "zzz"
    all_qubits = list(range(nb_qubits))
    l = [
        [nb_qubits, obs, ["+","-"], {"x": all_qubits, "y": all_qubits}],
        [nb_qubits, obs, ["+","-"], {"z": all_qubits}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r[0]== r[1]

def test_ZX_equivalent_to_Y():
    """Test de l'équivalence entre ZX et Y dans un circuit à 3 qubits."""
    nb_qubits = 3
    obs = "zzz"
    all_qubits = list(range(nb_qubits))
    l = [
        [nb_qubits, obs, ["+","-"], {"z": all_qubits, "x": all_qubits}],
        [nb_qubits, obs, ["+","-"], {"y": all_qubits}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r[0]== r[1]

def test_YZ_equivalent_to_X():
    """Test de l'équivalence entre YZ et X dans un circuit à 3 qubits."""
    nb_qubits = 3
    obs = "zzz"
    all_qubits = list(range(nb_qubits))
    l = [
        [nb_qubits, obs, ["+","-"], {"y": all_qubits, "z": all_qubits}],
        [nb_qubits, obs, ["+","-"], {"x": all_qubits}]
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r[0]== r[1]

def test_user_output():
    """Test afin de vérifier que l'utilisateur reçoit bien seulement les mesures reliées aux
    valeurs propres qu'il a demandées."""
    l = [
        [1, "z",  ["+"],     {"x": [0]}],
        [2, "zi", ["+", "-"],{"h": [0], "cx": [[0, 1]]}],
        [2, "zz", ["-"],     {"h": [0], "cx": [[0, 1]]}],
    ]
    results = [
        {"+": 0},             # Show only the measurement probability of the eigenvalue +1
        {"+": 0.5, "-": 0.5}, # Show the measurement probabilities of the eigenvalues +1 and -1
        {"-": 0}              # Show only the measurement probability of the eigenvalue -1
    ]
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)
    assert r == results
