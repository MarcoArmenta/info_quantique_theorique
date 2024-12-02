from observables import PauliObservable


conjugation_dict = {############## Fait avec ChatGPT
    # Conjugation by h
    ('h', 'x'): ('z', 1),
    ('h', 'z'): ('x', 1),
    ('h', 'y'): ('y', -1),
    ('h', 'i'): ('i', 1),

    # Conjugation by s
    ('s', 'x'): ('y', 1),
    ('s', 'y'): ('x', -1),
    ('s', 'z'): ('z', 1),
    ('s', 'i'): ('i', 1),

    # Conjugation by x
    ('x', 'x'): ('x', 1),
    ('x', 'y'): ('y', -1),
    ('x', 'z'): ('z', -1),
    ('x', 'i'): ('i', 1),

    # Conjugation by y
    ('y', 'x'): ('x', -1),
    ('y', 'y'): ('y', 1),
    ('y', 'z'): ('z', -1),
    ('y', 'i'): ('i', 1),

    # Conjugation by z
    ('z', 'x'): ('x', -1),
    ('z', 'y'): ('y', -1),
    ('z', 'z'): ('z', 1),
    ('z', 'i'): ('i', 1)
}

cnot_conjugation_dict = {############## Fait avec ChatGPT
    # Target = i
    ('i', 'i'): ['i','i', 1],          
    ('x', 'i'): ['x','x', 1],        
    ('y', 'i'): ['y','x', 1],       
    ('z', 'i'): ['z','i', 1],
    # Control = i  ','      
    ('i', 'x'): ['i','x', 1],          
    ('i', 'y'): ['z','y', 1],      
    ('i', 'z'): ['z','z', 1],        

    # Control = X
    ('x', 'x'): ['x','i', 1],        
    ('x', 'y'): ['y','z', 1],        
    ('x', 'z'): ['y','y', -1],       

    # Control = Z
    ('z', 'z'): ['i','z', 1],       
    ('z', 'y'): ['i','y', 1],       
    ('z', 'x'): ['z','x', 1],       

    # Control = Y
    ('y', 'y'): ['x','z', -1],       
    ('y', 'x'): ['y','i', 1],      
    ('y', 'z'): ['x','y', 1],      
 
}


class QuantumCircuit:
    """
    Classe qui prend en charge les portes Hadamard, S, CX et n'importe quelle porte de Pauli.
    """
    def __init__(self, l: list):
        self.circuits=l 
        self.generators=self.generators_evolution() #List of list of generators
        self.n_qubits=self.number_qubits()  #List of number of qubits per circuits
        self.eigen_values=self.eigen_val()  #List of list of eigenvalues for which we want probabilities
        self.observables=PauliObservable(self.circuits).observables()   #List of observable to measure

    
    def generators_evolution(self):
        """ 
        Returns list of list of generators for each circuits
        Generators are in the format {"qubit_number": operator}, example: {'0': z, '1', x, '2', i} for the 3 qubits generator zxi
        """
        generators=[] # List initialisation
        for circuit in self.circuits:   # Loops for each circuits
            n=circuit[0]    #Number of qubits in circuit
            op_list=circuit[3:] #List of gates
            stabs,factors,ops=[],[],[]  #List initialisation for stabilisator generators, factor (+1 or -1) and operators to apply

            for op_dict in op_list:     # Operators in string format
                for op in op_dict:
                    for qubit in op_dict[op]:
                        if op=='cx':
                            ops.append(str(op)+str(qubit[0])+str(qubit[1]))
                        else:
                            ops.append(str(op)+str(qubit))


            for qubit in range(n): # Generator initialisation (eg: ziii,izii,iizi,iiiz, for 4 qubits)
                dict_stab={}
                for i in range(n):
                    dict_stab[str(i)]='i'
                dict_stab[str(qubit)]='z'
                stabs.append(dict_stab)
                factors.append(1) # List to keep track if positive or negative, starts positive

            for idx,stab in enumerate(stabs):   # Conjugates each stabilizer generator using conjugation_dict if operator is x, y, z, h, s or conjugation_dict_cx if operator is cx
                for op in ops:
                    if op[0] in 'xyzhs':
                        stab[op[-1]],factor_temp=conjugation_dict[(op[0],stab[op[-1]])]
                        factors[idx]*=factor_temp
                    elif op[0:2]=='cx':
                        stab[op[-2]],stab[op[-1]],factor_temp=cnot_conjugation_dict[(stab[op[-2]],stab[op[-1]])]
                        factors[idx]*=factor_temp
                    
            for stab,fac in zip(stabs,factors):     # Adds a dictionnary entry for the phase (+ or -)
                if fac==1:
                    stab['phase']='+'
                elif fac==-1:
                    stab['phase']='-'
            generators.append(stabs)
        return generators


    def eigen_val(self):
        """ Returns list of list of eigenvalues for which we want the probabilities """
        eigenvalues=[]
        for circuit in self.circuits:
            eigenvalues.append(circuit[2])
        return eigenvalues
    
    
    def number_qubits(self):
        """ Returns list of number of qubits per circuits """
        nb_qubits=[]
        for circuit in self.circuits:
            nb_qubits.append(circuit[0])
        return nb_qubits
    

    