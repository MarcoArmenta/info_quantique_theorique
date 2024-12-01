import numpy as np
class GKSimulator:
    def __init__(self):
        return
    
    def run(self, circ):
        #Applies gates to |00...0> state, then measures observable
        self.update_gates(circ)
        return self.measure(circ)

    def update_gates(self, circ):
        #Applies gates
        for gate_set in circ.gates:
            for (gate, qubits) in gate_set.items():
                if gate =='h':
                    circ.h(qubits)
                elif gate =='s':
                    circ.h(qubits)
                elif gate =='cx':
                    circ.cx(qubits)
                elif gate == 'x':
                    circ.x(qubits)
                elif gate =='y':
                    circ.y(qubits)
                elif gate =='z':
                    circ.z(qubits)

    def measure(self, circ):
        #Checks if observable commutes with stabilizers, returns probability of specific eigenvalues
        temp_result = {}
        if circ.observ.commutes(circ.curr_stab):
            temp_result = np.random.choice([{"+1":1, "-1":0}, {"+1":0, "-1":1}])

        else:
            temp_result = {"+1":0.5, "-1":0.5}

        final_result = {}
        if '+' in circ.eigenvals:
            final_result['+1']=temp_result['+1']
        if '-' in circ.eigenvals:
            final_result['-1']=temp_result['-1']
        
        return final_result


