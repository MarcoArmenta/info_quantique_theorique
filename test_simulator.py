"""
Tests for the simulator module.
"""

import numpy as np
from pytest import mark

from benchmark_stim import benchmark_stim
from simulator import GKSimulator
from utils import generate_random_circuits


@mark.parametrize("num_rand_circuits", range(500))
def test_random_circuits_stim(num_rand_circuits):

    rng = np.random.default_rng()

    num_qubits = rng.integers(2, 20)
    num_blocks = rng.integers(1, 20)
    num_gates = rng.integers(1, 20)

    q = generate_random_circuits(1, num_qubits, num_blocks, num_gates)

    simulator = GKSimulator()
    simulator.evolve_tableau(
        q.num_qubits[0], q.gates[0], q.observables[0], q.eigenvalues[0]
    )
    sim_tab, sim_signs, sim_observable_expectation = (
        simulator.pauli,
        simulator.signs,
        simulator.observable_expectation,
    )

    stim_tab, stim_signs, stim_observable_expectation = benchmark_stim(q)

    assert np.array_equal(sim_tab, stim_tab)
    assert np.array_equal(sim_signs, stim_signs)
    assert sim_observable_expectation == stim_observable_expectation
