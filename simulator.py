from quantumcircuit import QuantumCircuit

class GKSimulator:
    def __init__(self):
        pass
    
    def run(self,quantum_circuits):
        quantum_circuits.run()
        quantum_circuits.measure_all()
        return quantum_circuits.eigen_value_l