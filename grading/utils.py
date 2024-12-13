import random
import pennylane as qml


def compare_results(p, q):
    return sum(r == t for r, t in zip(p, q))


def from_string_to_observable(observable_string):
    observable = qml.Identity(1) if observable_string[0] == 'i' else qml.PauliZ(0)
    for i, char in enumerate(observable_string[1:]):
        if char == 'z':
            observable = observable @ qml.PauliZ(i + 1)
        elif char == 'i':
            observable = observable @ qml.Identity(i + 1)
    return observable


def apply_circuit(num_qubits, observable, instructions):
    '''
        observable: string
        instructions: list of dictionaries {'x':[0,23,5233]}

        return expectation value of the observable on the constructed circuit
    '''
    dev = qml.device("default.clifford", wires=num_qubits, tableau=True)

    @qml.qnode(dev)
    def circuit():
        for gate in instructions:
            args = instructions[gate]
            if gate == 'x':
                for qubit in args:
                    qml.PauliX(wires=qubit)
            elif gate == 'y':
                for qubit in args:
                    qml.PauliY(wires=qubit)
            elif gate == 'z':
                for qubit in args:
                    qml.PauliZ(wires=qubit)
            elif gate == 's':
                for qubit in args:
                    qml.S(wires=qubit)
            elif gate == 'y':
                for qubit in args:
                    qml.PauliY(wires=qubit)
            elif gate == 'h':
                for qubit in args:
                    qml.Hadamard(wires=qubit)
            elif gate == 'cx':
                for arg in args:
                    qml.CNOT(wires=arg)

        return qml.expval(from_string_to_observable(observable))

    return circuit()


# This is an AI generated function
def calculate_eigenvalue_probability(observable_string, eigenvalue, circuit):
    num_qubits = len(observable_string)

    expectation_value = apply_circuit(num_qubits, observable_string, instructions=circuit)

    if eigenvalue == '+':
        return (1 + expectation_value) / 2
    elif eigenvalue == '-':
        return (1 - expectation_value) / 2
    else:
        raise ValueError("Invalid eigenvalue. Must be '+' or '-'.")


def generate_random_clifford_circuit(num_qubits, num_gates, reps=5):
    gates = {}
    for _ in range(reps):
        for _ in range(num_gates):
            gate_type = random.choice(['h', 's', 'x', 'y', 'z'])
            sample_size = random.randint(1, num_qubits)
            qubit_indexes = random.sample(range(num_qubits), sample_size)
            gates.update({gate_type: qubit_indexes})

        g = []
        for _ in range(num_gates):
            rn = random.randint(1, num_qubits)
            control_qubits = [random.randint(0, num_qubits - 1) for _ in range(rn)]
            target_qubits = [random.randint(0, num_qubits - 1) for _ in range(rn)]
            for c, t in zip(control_qubits, target_qubits):
                if c == t:
                    continue
                g.append([c, t])
        if len(g) > 0:
            gates.update({'cx': g})

    return gates



max_qubits = 50
circuits_to_simulate = []
for _ in range(100):
    n = random.randint(5, max_qubits)
    obs = random.choice(['z' + 'i'*(n-1),
                         'zzz' + 'i'*(n-3),
                         'i' * (n - 5) + 'zzzzz',
                         'z'*n,
                         'i'*(n-1) + 'z'])
    num_gates = random.randint(3, 10)
    reps = random.randint(3, 10)
    eigenvals = random.choice([['+'],
                               ['-'],
                               ['+', '-']])
    circ = [n, obs, eigenvals, generate_random_clifford_circuit(num_qubits=n, num_gates=num_gates, reps=reps)]
    circuits_to_simulate.append(circ)


import json
with open('grading_circuits.json', 'w') as f:
    json.dump(circuits_to_simulate, f)

results = []
for simulation in circuits_to_simulate:
    _, observable, eigenvalues, circuit_instructions = simulation
    auxiliary = {}
    for eigenval in eigenvalues:
        probs = calculate_eigenvalue_probability(observable, eigenval, circuit_instructions).item()
        auxiliary.update({eigenval: probs})

    results.append(auxiliary)

with open('results.json', 'w') as f:
    json.dump(results, f)

