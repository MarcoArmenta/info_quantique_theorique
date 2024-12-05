#Classe PauliObservables(Pauli)
import numpy as np

class PauliObservables: 
    def __init__(self, observable_string):
        self.observable = observable_string
        self.n = len(observable_string)
        self.x_table = np.zeros(self.n)
        x_index = [posx for posx, charx in enumerate(self.observable) if (charx == 'x' or charx =='y')] # Found on StackOverflow, returns a list of indices where there is an x or y
        self.x_table[x_index] = 1
        self.z_table = np.zeros(self.n)
        z_index = [posz for posz, charz in enumerate(self.observable) if (charz == 'z' or charz =='y')] # Found on StackOverflow, returns a list of indices where there is an z or y
        self.z_table[z_index] = 1
        self.phases = np.ones(self.n)
        y_index = [posy for posy, chary in enumerate(self.observable) if chary == 'y'] # Found on StackOverflow, returns a list of indices where there is a y
        self.x_table[y_index] = 1
        self.z_table[y_index] = 1
        self.phases = 1 - 2*(len(y_index)%2)


