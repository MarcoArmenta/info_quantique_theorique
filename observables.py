class PauliObservable:
    """
    Class représentant une observable de Pauli.
    """
    def __init__(self, l : list):
        self.circuits=l
        # pass

    def observables(self):
        """
            Returns list of dictionnary of observables in the format [{'as_string':'observables','qubit_number':'operator'}]
            Example: [{'as_string': '+zi', '0': 'z', '1': 'i'}, {'as_string': '-z', '0': 'z'}]
        """ 
        observables=[]
        for circuit in self.circuits:
            if circuit[1][0]=='-':
                observable={'as_string':circuit[1]}
                circuit[1]=circuit[1].replace('-','',1)
            elif circuit[1][0]=='+':
                observable={'as_string':circuit[1]}
                circuit[1]=circuit[1].replace('+','',1)
            else:
                observable={'as_string':'+'+circuit[1]}
            for idx,obs in enumerate(circuit[1]):
                observable[str(idx)]=obs

            observables.append(observable)
        return observables