from quantumcircuit import QuantumCircuit
from observables import PauliObservable
import json

class GKSimulator:
    def __init__(self):
        pass

    def charger_circuits(self, fichier_json):
        with open(fichier_json, 'r') as fichier:
            circuits = json.load(fichier)
        return circuits

    def exécuter_circuit(self, données_circuit):
        circuit = QuantumCircuit(données_circuit)
      
        return {"résultat": "Simulation effectuée"}

    def simuler(self):
        données_circuits = self.charger_circuits('chemin/vers/dummy_circuits.json')
        résultats = []
        for données in données_circuits:
            résultats.append(self.exécuter_circuit(données))
        return résultats
