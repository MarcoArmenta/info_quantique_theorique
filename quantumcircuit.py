from observables import PauliObservable

class QuantumCircuit:
    def __init__(self, datalist):
        self.circuits = []
        for list in datalist:
            self.circuits.append(IndivQuantumCircuit(list))

class IndivQuantumCircuit:
    def __init__(self, datalist):
        self.num_qubits = datalist[0]
        self.observ = PauliObservable(datalist[1])
        self.eigenvals = datalist[2]
        self.gates = datalist[3:]
        self.curr_stab = [PauliObservable(''.join(['i' for _ in range(i)]) +'z'+''.join(['i' for _ in range(i+1, self.num_qubits)])) for i in range(self.num_qubits)]
    
    def h(self, qubits):
        update = {'x': 'z', 'y':'y', 'z':'x', 'i':'i'}
        for (i, stab) in enumerate(self.curr_stab):
            for q in qubits:
                self.curr_stab[i].observ = stab.observ[:q]+update[stab.observ[q]]+stab.observ[q+1:]

    def s(self, qubits):
        update = {'x': 'y', 'y':'x', 'z':'z', 'i':'i'}
        for (i, stab) in enumerate(self.curr_stab):
            for q in qubits:
                self.curr_stab[i].observ = stab.observ[:q]+update[stab.observ[q]]+stab.observ[q+1:]


    def cx(self, qubits):
            update = {'xy': 'yz', 'yx':'yi', 'xz':'yy', 'zx':'zx', 'yz':'xy', 'zy':'iy', 'xi':'xx', 'ix':'ix', 'yi':'yx', 'iy':'zy', 'zi':'zi', 'iz':'zz', 'ii':'ii', 'zz': 'iz', 'yy': 'xz', 'xx': 'xi'}
            for (i, stab) in enumerate(self.curr_stab):
                for q in qubits:
                    new = update[stab.observ[q[0]]+stab.observ[q[1]]]
                    self.curr_stab[i].observ = stab.observ[:q[0]]+new[0]+stab.observ[q[0]+1:]
                    self.curr_stab[i].observ = stab.observ[:q[1]]+new[1]+stab.observ[q[1]+1:]

    def x(self, qubits):
        for (i, stab) in enumerate(self.curr_stab):
            for q in qubits:
                if self.curr_stab[i].observ[q] != 'x':
                    self.curr_stab[i].phase = not self.curr_stab[i].phase
        
    
    def y(self, qubits):
        for (i, stab) in enumerate(self.curr_stab):
            for q in qubits:
                if self.curr_stab[i].observ[q] != 'y':
                    self.curr_stab[i].phase = not self.curr_stab[i].phase


    def z(self, qubits):
        for (i, stab) in enumerate(self.curr_stab):
            for q in qubits:
                if self.curr_stab[i].observ[q] != 'y':
                    self.curr_stab[i].phase = not self.curr_stab[i].phase


