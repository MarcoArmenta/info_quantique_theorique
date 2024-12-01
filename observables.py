import numpy as np
class PauliObservable:
    def __init__(self, observ):
        if observ[0]=='-':
            self.phase =True
            self.observ = observ[1:]
        else:
            self.phase =False
            self.observ = observ
    
    def check_commute(self, A, B):
        #returns True if A and B commute, False otherwise
            commutator = np.dot(A, B) - np.dot(B, A)
            return np.allclose(commutator, np.zeros_like(commutator))
        
    def commutes(self, stabs):
        #returns True self commutes with all stabilizers in stabs, False otherwise
        pmats = {'i':np.array([[1, 0], [0, 1]]), 'x':np.array([[0, 1], [1, 0]]), 'y':np.array([[0, -1j], [1j, 0]]), 'z':np.array([[1, 0], [0, -1]])}
        for stab in stabs:
            for (i, j) in zip(stab.observ, self.observ):
                if not self.check_commute(pmats[i], pmats[j]):
                    return False
        return True