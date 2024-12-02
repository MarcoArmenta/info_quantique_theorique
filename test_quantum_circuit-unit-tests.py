import unittest
import json
import stim  # Stim est utilisé pour comparer les résultats
from simulator import GKSimulator
from quantumcircuit import QuantumCircuit

class TestQuantumSimulatorWithStim(unittest.TestCase):

    def setUp(self):
        """
        Chargement du fichier JSON avec 20 circuits pour les tests.
        (GENERER PAR gpt-4o)
        """
        with open("test_circuits.json", "r") as file:  # Changez le chemin si nécessaire
            self.circuits_data = json.load(file)

    def convert_to_stim(self, circuit_data):
        """
        Convertit un circuit décrit dans le fichier JSON en un circuit compatible avec Stim.
        """
        stim_circuit = stim.Circuit()
        circuits_list = circuit_data[3:]
        for circuit in circuits_list:
            for gate, targets in circuit.items(): #(cette boucle GENERER PAR gpt-4o)
                if gate == "h":
                    for target in targets:
                        stim_circuit.append_operation("H", [target])
                elif gate == "s":
                    for target in targets:
                        stim_circuit.append_operation("S", [target])
                elif gate == "cx":
                    for control, target in targets:
                        stim_circuit.append_operation("CNOT", [control, target])
                elif gate in ["x", "y", "z"]:
                    for target in targets:
                        stim_circuit.append_operation(gate.upper(), [target])
        return stim_circuit

    def test_compare_with_stim(self):
        """
        Compare les résultats du simulateur avec ceux de Stim pour chaque circuit.
        """
        simulator = GKSimulator()
        
        q_circuit = QuantumCircuit(self.circuits_data)
        result = simulator.run(q_circuit)

        for circuit_data in self.circuits_data: #(cette boucle GENERER PAR gpt-4o)
            

            # Conversion en circuit Stim
            stim_circuit = self.convert_to_stim(circuit_data)

            # Configuration de l'état initial et mesure
            observable = circuit_data[1]  # Observable de Pauli
            num_qubits = circuit_data[0]

            # Stim: Simule les résultats des mesures pour chaque Pauli observable
            stim_results =[]
            stim_result = {}
            for eigenvalue in circuit_data[2]:
                if eigenvalue == "+":
                    meas_pauli = stim.PauliString(observable)
                elif eigenvalue == "-":
                    meas_pauli = -stim.PauliString(observable)
                else:
                    raise ValueError("Valeur propre non prise en charge.")

                # Simulation avec Stim
                stim_result[eigenvalue] = stim_circuit.measure_ket(
                    num_shots=1000,  # Utilisez des échantillons pour estimer les probabilités
                    pauli_observable=meas_pauli,
                )
            stim_results.append(stim_result)

        # Vérification des résultats
        
        for i in range(len(result)):
            for eigenvalue, prob in stim_results[i].items(): #(cette boucle GENERER PAR gpt-4o)
                self.assertAlmostEqual(
                    result[i][eigenvalue],
                    prob,
                    places=2,
                    msg=f"Les probabilités pour {eigenvalue} ne correspondent pas (GKSimulator vs Stim)."
                )

if __name__ == "__main__":
    unittest.main()
