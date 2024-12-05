#Classe GKSimulator(QuantumCircuit)
#   method Pauli -> mesure

from observables import PauliObservables
from quantumcircuit import QuantumCircuit

class GKSimulator:

    def __init__(self, circuit):
        self.gates = circuit.gates_list
        self.observable = PauliObservables(circuit.observable)
        return
    
    def commutation(self, circuit):
        commutator = 0;
        for i in range(circuit.n):
            circuit_z = circuit.z_table["z"+str(i)]
            circuit_x = circuit.x_table["x"+str(i)]

        # This verification of the commutation has been made with ChatGPT, by explaining the stabilizers tableau and asking it how to get the sympletic produt
            commutator = (sum(x * z for x, z in zip(self.observable.x_table, circuit_z)) +sum(z * x for z, x in zip(self.observable.z_table, circuit_x))) % 2
            if commutator == 1:  # observable commutes with at least one stabilizer
                return False

        #If all commutes
        return True
            


    def run(self, circuit):
        "This section of the function has been generated with chatGPT"
        for gate_dict in self.gates:
            for gate, targets in gate_dict.items():
               

                #This section is my own
                if gate == 'x':
                    circuit.x(targets)
            
                elif gate == 'y':
                    circuit.y(targets)
                
                elif gate == 'z':
                    circuit.z(targets)

                elif gate == 's':
                    circuit.s(targets)

                elif gate == 'h':
                    circuit.h(targets)

                elif gate == 'cx':
                    circuit.cx(targets)
            circuit.get_stabilizers()

        if self.commutation(circuit):

            results = {}
            #print("commute")

            #Recherche de +/- observable dans le stabilizateur
            search = False
            i=0
            while (i<circuit.n and search == False):
                #print("circuit stabs",circuit.x_table, "obs", self.observable.x_table,"obs phase=", self.observable.phases)
                #Si l'observable est directement dans la liste de générateurs
                if (all(circuit.x_table["x"+str(i)] == self.observable.x_table) and all(circuit.z_table["z"+str(i)] == self.observable.z_table )): 
                
                    #Arrêter la recherche, vérifier la parité et retourner le résulta {+}=1 ou {-}=1 en fonction
                    search = True
                    #print("found in")
                    parity = self.observable.phases*circuit.phases[i]

                else: 
                    for j in range(circuit.n):
                        g_xProd = (circuit.x_table["x"+str(i)] + circuit.x_table["x"+str(j)])%2 
                        g_zProd = (circuit.z_table["z"+str(i)] + circuit.z_table["z"+str(j)])%2   
                        g_phasesProd = circuit.phases[i] * circuit.phases[j]
                        #print(g_phasesProd)
                        if (all(g_xProd == self.observable.x_table) and all(g_zProd == self.observable.z_table)):
                            search = True 
                            parity = g_phasesProd * self.observable.phases
                            #print("found prod", parity)
                        else: 
                            parity = -1
                            search = True
                i+=1
                

            
            for eigenval in circuit.eigenvals:
                #print(eigenval, parity)
                if (eigenval == "+" and parity == 1):
                    results["+"] = 1
                elif (eigenval == "-" and parity == -1):
                    results["-"]= 1
                else: 
                    results[eigenval] = 0
    
                        
                
            return results
            

        elif self.commutation(circuit) == False:
            results = {}
            for eigenval in circuit.eigenvals:
                results[eigenval] = 0.5
            #print(results)
            #print("no commute")
            return results

    
