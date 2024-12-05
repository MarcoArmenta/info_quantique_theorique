import numpy as np

class QuantumCircuit:
    '''Inspired from [1], but using a dictionnary with x,z and the stabilizers instead of a Tableau to help me visualize my mistakes better while coding. I then removed the dictionary of stabilizers and the keys in my x and z table to save memory and time
     I used ChatGPT to understand the "Tableau" formalism and help with OOP (__init__, self, etc.)'''
   
    #Initializing the number of qbits, x,z and phases tables, getting the gates_list from the circuit
    def __init__(self, circuit):
        self.n = circuit[0]
        self.x_table = {'x'+str(i): np.zeros(self.n) for i in range(self.n)}
        self.z_table = {'z'+str(j): np.zeros(self.n) for j in range(self.n)}
        for i in range(self.n):
            self.z_table['z'+str(i)][i] = 1
        self.phases = np.ones(self.n)
        self.stabilizers = {'s'+str(k): np.zeros(2*self.n + 1, dtype = int) for k in range(self.n)}
        self.gates_list = circuit[3:]
        self.eigenvals = circuit[2]
        self.observable = circuit[1]
    
    def get_stabilizers(self):
    #Updating stabilizers with x, z and phase table
        for i in range(self.n):
            for j in range(self.n):
                self.stabilizers['s'+str(i)][2*j]= self.x_table['x'+str(i)][j]
                self.stabilizers['s'+str(i)][2*j+1]= self.z_table['z'+str(i)][j]
            self.stabilizers['s'+str(i)][-1] = self.phases[i]
        print("get_stabl",self.stabilizers)
        


    def x(self, targets):
        #x -> x 
        #z -> -z 
        for target in targets:
            for i in range(self.n):
                #Multiply the phase by -1 if z
                if self.z_table['z'+str(i)][target]:
                    self.phases[i] *= -1
            #print("applied x to", target)

    def y(self, targets):
        #x -> -x
        #z -> -z
        for target in targets:
            for i in range(self.n):
                if self.x_table['x'+str(i)][target]:
                    self.phases[i] *= -1
                if self.z_table['z'+str(i)][target]: 
                    self.phases[i] *= -1
    
    def z(self, targets): 
        #x -> -x 
        #z -> z
        for target in targets: 
            for i in range(self.n):
                if self.x_table['x'+str(i)][target]:
                    self.phases[i] *= -1

    def h(self, targets):
        #x -> z 
        #z -> x
         for target in targets: 
            for i in range(self.n):
                self.x_table['x'+str(i)][target], self.z_table['z'+str(i)][target] = self.z_table['z'+str(i)][target], self.x_table['x'+str(i)][target]
                if (self.x_table['x'+str(i)][target] == 1 and self.z_table['z'+str(i)][target] == 1):
                    self.phases[i] *=-1
            #print("applied h to", target)

    def s(self, targets): 
        #x -> -xz 
        #z -> z
        for target in targets:
            for i in range(self.n):
                if self.x_table['x'+str(i)][target]:
                    temp = self.z_table['z'+str(i)][target] + 1
                    self.z_table['z'+str(i)][target] = temp%2
                    self.phases[i] *= -1
            #print("applied s to", target)

    def cx(self, targets):
        # x_control -> x_control x_target
        # x_target -> x_target
        # z_control -> z_control 
        # z_target -> z_control z_target
        
        for control, target in targets:
            for i in range(self.n):
                if self.x_table['x'+str(i)][control]:
                    tempx = self.x_table['x'+str(i)][target] + 1
                    self.x_table['x'+str(i)][target] = tempx%2
                if self.z_table['z'+str(i)][target]:
                    tempz = self.z_table['z'+str(i)][control] + 1
                    self.z_table['z'+str(i)][control] = tempz%2
            #print("applied cx to", targets)


    



    
