from quantumcircuit import QuantumCircuit
from pauliobservable import PauliObservable
from multiprocessing import Pool, cpu_count
import json

class GKSimulator:
    def __init__(self):
        pass

    def charger_circuits(self, CJ): # code généré par l'IA pour ouvrir le fichier json
        with open('CJ.json', 'r') as f:
            circuits = json.load(f)
        return circuits

    def verifier_commutateurs(self, circuit, observable): # vérification de la commutation
        px_pz = observable.convertir_en_px_pz()
        #print(f"Observable convertie : P_x = {px_pz['P_x']}, P_z = {px_pz['P_z']}")
        P_x = px_pz['P_x']
        P_z = px_pz['P_z']
        # calcul du commutateur
        commutateurs = []
        for stabilisateur in circuit.stabilisateur:
            V_x = stabilisateur['V_x']
            V_z = stabilisateur['V_z']
            s = stabilisateur['s']
            commutateur = 0
            for i in range(len(V_x)):
                commutateur = (V_x[i] * P_z[i] - V_z[i] * P_x[i]) % 2 # le calcul a été fait en prenant des termes croisés
            commutateurs.append((commutateur,s))
        #print(f"Commutateurs calculés : {commutateurs}")
        return commutateurs


    def mesurer_observable(self, circuit, observable): # Analyse du commutateur
        commutateurs = self.verifier_commutateurs(circuit, observable)

        if commutateurs == [(0,0)] * len(commutateurs):  # Tous les commutateurs sont nuls
            px_pz = observable.convertir_en_px_pz()
            P_x, P_z = px_pz['P_x'], px_pz['P_z']

            for stabilisateur in circuit.stabilisateur:
                if stabilisateur['V_x'] == P_x and stabilisateur['V_z'] == P_z :
                    if stabilisateur['s'] == 0 :
                        return {"+": 1}  #  probabilité de mesurer la valeur propore + est 1
                    else :
                        return {"-": 1}  #  probabilité de mesurer la valeur propore - est 1      
            return {"+": 0.5, "-": 0.5}  # deux valeurs propres possibles \pm1 avec une probabilité équiprobables pour les deux valeurs propres.
        
        # pas de commutation ###### nouvelles modifications au code
        probabilités = {"+": 0, "-": 0}        
        for stabilisateur in circuit.stabilisateur :
            if stabilisateur['s'] == 0:
                probabilités["+"] = probabilités["+"] + 0.5
            else:
                probabilités["-"] = probabilités["-"] + 0.5
        
        # normalisation
        normalisation = probabilités["+"] + probabilités["+"]
        probabilités["+"] = probabilités["+"] / normalisation
        probabilités["-"] = probabilités["-"] / normalisation

        if probabilités["-"] == 1:
            return {"-": probabilités["-"]}  # retourne la probabilité de "-"
        elif probabilités["-"] == 1:
            return {"+": probabilités["+"]}  # retourne la probabilité de "+"

        return probabilités

    def simuler_circuit(self, circuit_data):
        n_qubits = circuit_data[0] # Nombre de qubits extrait du fichier json
        observable_pauli = PauliObservable(circuit_data[1])  # Observable extraites du fichier json
        portes = circuit_data[3] # Portes quantiques extraites du fichier json

        # Initialiser le circuit
        circuit = QuantumCircuit([n_qubits])

        # Appliquer les portes
        if "h" in portes:
            for qubit in portes["h"]:
                circuit.application_hadamard(qubit)
        if "cx" in portes:
            for cible, controle in portes["cx"]:
                circuit.CX(cible, controle)
        if "s" in portes:
            for qubit in portes["s"]:
                circuit.application_de_S(qubit)
        if "x" in portes:
            for qubit in portes["x"]:
                circuit.application_de_pauli(qubit, 'X')
        if "y" in portes:
            for qubit in portes["y"]:
                circuit.application_de_pauli(qubit, 'Y')
        if "z" in portes:
            for qubit in portes["z"]:
                circuit.application_de_pauli(qubit, 'Z')

        # Mesurer l'observable
        resultat = self.mesurer_observable(circuit, observable_pauli)
        return resultat

    def run(self, fichier_json):
        circuits_data = self.charger_circuits(fichier_json)

        # Utiliser un pool de processus pour la simulation parallèle  # code généré par l'IA. Mon code a du être modifié car d'après ce que j'ai compris, le multiprocess ne peut pas lire de liste, du coup j'ai séparé les simulations, un pour un circuit, puis l'autre pour la liste.
        with Pool(processes=2) as pool: # ici remplacer cpu_count() par le nombre de coeur souhaité
            resultats = pool.map(self.simuler_circuit, circuits_data)

            retun(resultats)
