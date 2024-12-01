"""
Auteur: Jérémie Boudreault
"""
import multiprocessing as mp
import numpy as np
from observables import PauliObservable


class GKSimulator:
    """
    Classe qui crée un simulateur contenant une méthode run
    qui prend en argument un quantum circuit et qui permet de
    mesurer une observable donnée. Le simulateur fonctionne avec
    la méthode des tableaux.
    """
    def __init__(self):
        return

    def get_initial_table(self, n):
        """

        :param n: number of qubits
        :return: the initial table corresponding to the state |0>^tensor(n)
        """
        i_table = np.append(np.identity(2*n), np.zeros((2*n, 1)), axis=1)
        return i_table

    def apply_cx(self,table,targets):
        n = int(table.shape[0] / 2)
        for target in targets:
            launch, land = target
            table[:, -1] = (table[:, -1] + (table[:, launch] * table[:, land + n]) *
                            ((table[:, land] + table[:, launch + n] + 1) % 2)) % 2  # set r_i = r_i + x_ia*z_ia*(x_ib + z_ia + 1)

            table[:, land] = (table[:, land] + table[:, launch]) % 2  # set x_ib = x_ib + x_ia
            table[:, launch + n] = (table[:, launch + n] + table[:, land + n]) % 2  # set z_ia = z_ia + z_ib
            return table

    def apply_h(self,table,targets):
        n = int(table.shape[0] / 2)
        for target in targets:
            table[n:, -1] = (table[n:, -1] + table[n:, target] * table[n:,target + n]) % 2  # set r_i = r_i + x_ia*z_ia
            x_ia, z_ia = np.copy(table[n:, target]), np.copy(table[n:, target + n])
            table[n:, target], table[n:, target + n] = z_ia, x_ia  # swap x_ia and z_ia
        return table

    def apply_s(self,table,targets):
        n = int(table.shape[0] / 2)
        for target in targets:
            table[n:, -1] = (table[n:, -1] + table[n:, target] * table[n:,
                                                                     target + n]) % 2  # set r_i = r_i + x_ia*z_ia
            table[n:, target + n] = (table[n:, target + n] + table[n:,
                                                                     target]) % 2  # set z_ia = z_ia + x_ia
        return table

    def apply_z(self,table,targets):
        table = self.apply_s(self.apply_s(table, targets), targets)
        return table

    def apply_x(self,table, targets):
        table = self.apply_h(self.apply_z(self.apply_h(table, targets), targets), targets)
        return table

    def apply_y(self,table,targets):
        table = self.apply_s(self.apply_s(self.apply_s(self.apply_x(self.apply_s(table, targets),
                                                                    targets), targets), targets), targets)
        return table

    def apply_gate(self,table,gate,targets):
        """

        :param table:
        :param gate:
        :param targets:
        :return:
        """
        if gate == 'cx':
            table = self.apply_cx(table, targets)
        if gate == 'h':
            table = self.apply_h(table, targets)
        if gate == 's':
            table = self.apply_s(table,targets)
        if gate == 'z':
            table = self.apply_z(table,targets)
        if gate == 'y':
            table = self.apply_y(table,targets)
        if gate == 'x':
            table = self.apply_x(table,targets)
        return table

    def apply_circuit(self, table, gates_dict):
        """

        :param table:
        :param gates_dict:
        :return:
        """
        for gate, targets in gates_dict.items():
            table = self.apply_gate(table, gate, targets)
        return table

    def g_func(self, x1, z1, x2, z2):
        if x1 == z1 == 0:
            value = 0
        elif x1 == z1 == 1:
            value = z2 - x2
        elif x1 == 1 and z1 == 0:
            value = z2*(2*x2 - 1)
        elif x1 == 0 and z1 == 1:
            value = x2*(1 - 2*z2)
        return value

    def row_sum(self, h, i, table):
        n = int(table.shape[0] / 2)
        r_h, r_i = table[h, -1], table[i, -1]
        sum_val = 2*r_h + 2*r_i + sum([self.g_func(table[i, j], table[i, j+n], table[h, j], table[h, j+n])
                                       for j in range(n)])
        if sum_val % 4 == 0:
            table[h, -1] = 0
        elif sum_val % 4 == 2:
            table[h, -1] = 1
        table[h, :2*n] = (np.copy(table[i, :2*n]) + np.copy(table[h, :2*n])) % 2
        return table

    def measurement(self, table, Os, values):
        n = int(table.shape[0]/2)
        # check if p exists such as prod(x_pa for all a that are z in Os) = 1
        po = PauliObservable(Os).paulis_vec
        if sum(po) == 1:
            zs = po[n:]
            x_ixs = np.where(zs)[0]
            p_bools = np.prod(table[n:, x_ixs], axis=1)
            # case I
            if np.array(p_bools).any():
                out = [values, [0.5]*len(values)]
            # case II
            else:
                table = np.append(table, np.zeros((1, 2*n+1)), axis=0)
                for i in range(n):
                    if np.prod(table[i, x_ixs]):
                        table = self.row_sum(2*n, i+n, table)
                result = table[-1, -1]
                probs = []
                for value in values:
                    if value == "+" and result == 0:
                        prob = 1
                    elif value == "+" and result == 1:
                        prob = 0
                    if value == "-" and result == 0:
                        prob = 0
                    if value == "-" and result == 1:
                        prob = 1
                    probs.append(prob)
                out = [values, probs]
        else:
            stabs = table[n:, :2*n].tolist()
            po = po.tolist()
            if po in stabs:
               ix = stabs.index(po)
               result = table[n:, -1][ix]
               probs = []
               for value in values:
                   if value == "+" and result == 0:
                       prob = 1
                   elif value == "+" and result == 1:
                       prob = 0
                   if value == "-" and result == 0:
                       prob = 0
                   if value == "-" and result == 1:
                       prob = 1
                   probs.append(prob)
               out = [values, probs]
            else:
                out = [values, [0.5]*len(values)]
        return out

    def worker(self, qc):
        n, Os, eig_vals, gates_dict = qc
        table = self.get_initial_table(n)
        evolved_table = self.apply_circuit(table, gates_dict)
        values, probs = self.measurement(evolved_table, Os, eig_vals)
        # measurement
        result = {value + "1": prob for value, prob in zip(values, probs)}
        return result

    def run(self, q):
        """
        Function that simulates the quantum circuit and get the expected probabilities
        associated with some eigenvalues.
        :param q: QuantumCircuit object
        :return: List of dictionaries of eigenvalues and their associated probability
        """
        qcs = q.qc
        if len(qcs) <= 8:
            core_count = len(qcs)
        else:
            core_count = 8
        print(f"USING {core_count} CORES")

        pool = mp.Pool(processes=core_count)
        results = [pool.apply(self.worker, args=[qc]) for qc in qcs]

        return results




