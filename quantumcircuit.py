import numpy as np
from observable import PauliObservable 


class QuantumCircuit:
    def __init__(self, l):
        self.num_circuits = len(l)
        self.stabs_l = []
        self.num_qubits_l = []
        self.observables_l = []
        self.gates_l = []
        self.eigen_value_l = []
        for elem in l :
            self.num_qubits_l.append(elem[0])
            
            observable = PauliObservable(elem[1])
            observable.initialize()
            self.observables_l.append(observable)
            
            eigenvalue = {}
            for value in elem[2] :
                eigenvalue.update({value : 0})
            self.eigen_value_l.append(eigenvalue)
            
            list_of_gates = []
            for i in range(3,len(elem)) :
                list_of_gates.append(elem[i])
            self.gates_l.append(list_of_gates)
            
            
            tab = StabilizerTableau(elem[0])
            tab.initialize()
            self.stabs_l.append(tab)
            
       
        
    def __repr__(self):
        """
        Représente le tableau stabilisateur de manière lisible.
        """
        return f"Stabilizer Tableau:\n{self.eigen_value_l}"
    
    
    def run(self):
        for i in range(self.num_circuits):
            for dict_gate in self.gates_l[i] :
                for gates, qubits in dict_gate.items():
                    if ( gates == 'x'):
                        for j in qubits : 
                            self.stabs_l[i].apply_X(j)
                    elif ( gates == 'z'):
                        for j in qubits :
                            self.stabs_l[i].apply_Z(j)
                    elif ( gates == 'y'):
                        for j in qubits :
                            self.stabs_l[i].apply_Y(j)
                    elif ( gates == 's'):
                        for j in qubits :
                            self.stabs_l[i].apply_S(j)
                    elif ( gates == 'h'):
                        for j in qubits :
                            self.stabs_l[i].apply_H(j)
                    elif ( gates == 'cx'):
                        for j in qubits :
                            self.stabs_l[i].apply_CX(j[0], j[1])
 
    def measure_all(self):
        for i in range(self.num_circuits):
            self.measure(i)
        return
    
    def measure(self, index):
        parity_result = 0
        commute_with_all_stabilisateur = True
        tableau_observable = self.observables_l[index].get_tableau()
        tableau_stabs = self.stabs_l[index].get_tableau()
        n_qubits = self.num_qubits_l[index]
        stab_commuting = []
        for i in range(n_qubits):
            interact = False
            commute = True
            # Observable is in the Stabilisateur Tab
            if np.array_equal(tableau_stabs[i][:2*n_qubits],tableau_observable[:2*n_qubits]) : 
                if ((tableau_stabs[i][-1] + tableau_observable[-1])% 2 == 0):
                    if '+' in self.eigen_value_l[index]:
                        self.eigen_value_l[index]['+'] = 1
                else :
                    if '-' in self.eigen_value_l[index]:
                        self.eigen_value_l[index]['-'] = 1
                return
            for j in range(n_qubits):
                if ((tableau_stabs[i][j] == 0 and tableau_stabs[i][j+n_qubits] == 0) 
                    or (tableau_observable[j] == 0 and tableau_observable[j+n_qubits] == 0)) :
                    pass
                elif (tableau_stabs[i][j] == tableau_observable[j] and 
                    tableau_stabs[i][j+n_qubits] == tableau_observable[j+n_qubits]):
                    interact = True
                else :
                    commute_with_all_stabilisateur = False
                    commute = False
            if (commute and interact): 
                stab_commuting.append(tableau_stabs[i])
        
        
        phases = np.array([stab[-1] for stab in stab_commuting])
        parity_result = np.sum(phases) + tableau_observable[-1] % 2
        
        
        if (commute_with_all_stabilisateur) :

            if (parity_result == 0):
                if '+' in self.eigen_value_l[index]:
                    self.eigen_value_l[index]['+'] = 1
            else :
                if '-' in self.eigen_value_l[index]:
                    self.eigen_value_l[index]['-'] = 1
            return
        else :
            if (len(stab_commuting) > 0):
                somme_mod_2 = np.bitwise_xor.reduce(stab_commuting)
                if np.array_equal(somme_mod_2[:2*n_qubits],tableau_observable[:2*n_qubits]) : 
                    if (parity_result == 0):
                        if '+' in self.eigen_value_l[index]:
                            self.eigen_value_l[index]['+'] = 1
                    else :
                        if '-' in self.eigen_value_l[index]:
                            self.eigen_value_l[index]['-'] = 1
                    return
            
            if '+' in self.eigen_value_l[index]:
                self.eigen_value_l[index]['+'] = 0.5
            if '-' in self.eigen_value_l[index]:
                self.eigen_value_l[index]['-'] = 0.5
            return
 
class StabilizerTableau:
    def __init__(self, n_qubits):
        self.n = n_qubits
        self.tableau = np.zeros((n_qubits, 2 * n_qubits  + 1), dtype=int)
        self.phase = np.array([[0, 1, 2, 3],
                  [1, 0, 3, 2],
                  [2, 3, 1, 0],
                  [3, 2, 0, 1]])

    def initialize(self):
        for i in range(self.n):
            
            self.tableau[i, self.n + i] = 1  

        
        self.tableau[:, -1] = 0  
    
        
    def update_phase(self,a,b):
        return self.phase[a][b]
    
                
    def get_tableau(self):
        return self.tableau

    def __repr__(self):
        """
        Représente le tableau stabilisateur.
        """
        return f"Stabilizer Tableau:\n{self.tableau}"
    
    def apply_X(self, qubit):
        #Z -> -Z and Y -> -Y
        for i in range(self.n):
            if (self.tableau[i, self.n + qubit] == 1):
                self.tableau[i, -1] = self.update_phase(self.tableau[i, -1],1)
            
            
    def apply_Z(self, qubit):
        #X -> -X and Y -> -Y
        for i in range(self.n):
            if (self.tableau[i, qubit] == 1):
                self.tableau[i, -1] = self.update_phase(self.tableau[i, -1],1) 
            
    def apply_Y(self, qubit):
        for i in range(self.n):
            #X -> -X
            if (self.tableau[i, qubit] == 1):
                self.tableau[i, -1] = self.update_phase(self.tableau[i, -1],1)  
            #Z -> -Z
            if (self.tableau[i, self.n + qubit] == 1):
                self.tableau[i, -1] = self.update_phase(self.tableau[i, -1],1) 
            
    def apply_H(self, qubit):
        for i in range(self.n):
            #Y -> -Y
            if (self.tableau[i, qubit] == 1 and self.tableau[i, self.n + qubit] == 1):
                self.tableau[i, -1] = self.update_phase(self.tableau[i, -1],1)
            #X -> Z -> X
            self.tableau[i, qubit], self.tableau[i, self.n + qubit] = self.tableau[i, self.n + qubit], self.tableau[i, qubit]
        
        
    def apply_S(self,qubit):
        for i in range(self.n):
            # X -> Y -> -X -> -Y
            if (self.tableau[i, qubit] == 1):
                self.tableau[i, self.n + qubit] = 1 - self.tableau[i, self.n + qubit]
                self.tableau[i, -1] = self.update_phase(self.tableau[i, -1],2)
            
    def apply_CX(self, control, target):
        for i in range(self.n):
            self.conjugateCX(i, control, target)
            
    
    def conjugateCX(self,qubit,control,target):
        #ZZ -> IZ -> ZZ
        if (self.tableau[qubit,target+self.n] == 1 and self.tableau[qubit,target] == 0 and 
            self.tableau[qubit,control] == 0 ):
            self.tableau[qubit,control+self.n] ^= 1
            return
        #XX -> XI -> XX
        if (self.tableau[qubit,control] == 1 and self.tableau[qubit,control+self.n] == 0 and 
            self.tableau[qubit,target+self.n] == 0 ):
            self.tableau[qubit,target] ^=1
            return
        #YY = -XZXZ -> -XZ
        if (self.tableau[qubit,control] == 1 and self.tableau[qubit,control+self.n] == 1 and
            self.tableau[qubit,target] == 1 and self.tableau[qubit,target+self.n] == 1):
            self.tableau[qubit,control + self.n] = 0 
            self.tableau[qubit,target] = 0
            return
        #-XZ -> -YY = XZXZ
        if (self.tableau[qubit,control] == 1 and self.tableau[qubit,control+self.n] == 0 and
            self.tableau[qubit,target] == 0 and self.tableau[qubit,target+self.n] == 1):
            self.tableau[qubit,control + self.n] = 1 
            self.tableau[qubit,target] = 1
            self.tableau[qubit, -1] = self.update_phase(self.tableau[qubit, -1],1)
            return
        #ZY -> IY -> ZY
        if (self.tableau[qubit,target+self.n] == 1 and self.tableau[qubit,target] == 1 and 
            self.tableau[qubit,control] == 0 ):
            self.tableau[qubit,control+self.n] ^= 1
            return
        #YZ -> XY 
        if (self.tableau[qubit,control] == 1 and self.tableau[qubit,control+self.n] == 1 and
            self.tableau[qubit,target] == 0 and self.tableau[qubit,target+self.n] == 1):
            self.tableau[qubit,control+self.n] = 0
            self.tableau[qubit,target] = 1
            return
        #XY -> YZ
        if (self.tableau[qubit,control] == 1 and self.tableau[qubit,control+self.n] == 0 and
            self.tableau[qubit,target] == 1 and self.tableau[qubit,target+self.n] == 1):
            self.tableau[qubit,control+self.n] = 1
            self.tableau[qubit,target] = 0
            return
        #YX -> YI -> YX
        if (self.tableau[qubit,control] == 1 and self.tableau[qubit,control+self.n] == 1 and 
            self.tableau[qubit,target+self.n] == 0 ):
            self.tableau[qubit,target] ^=1
            return
