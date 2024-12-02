import numpy as np

class PauliObservable:
    def __init__(self, string):
        self.size = len(string)
        self.stab = np.zeros(2*self.size+1, dtype=int)
        self.string = string
        self.phase = np.array([[0, 1, 2, 3],
                  [1, 0, 3, 2],
                  [2, 3, 1, 0],
                  [3, 2, 0, 1]])
    
    def initialize(self):
        for i in range(self.size):
            if self.string[i] == 'x':
                self.stab[i] = 1
            elif self.string[i] == 'z':
                self.stab[i+self.size] = 1
            elif self.string[i] == 'y':
                self.stab[i] = 1
                self.stab[i+self.size] = 1
                self.stab[-1] = self.update_phase(self.stab[-1], 2)
    
    def __repr__(self):
        """
        Représente le tableau stabilisateur de manière lisible.
        """
        return f"{self.stab}"
    
    def update_phase(self,a,b):
        return self.phase[a][b]
    
    def get_tableau(self):
        return self.stab