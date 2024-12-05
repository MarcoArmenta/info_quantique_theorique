# simulator
import numpy as np
from multiprocessing.pool import Pool
import time

class GKSimulator:
    def __init__(self):
        pass

    def _Single_circ_run(self, circ):
        # For every run we create the full tableau with destabilizer, stabilizer et signs
        Tableau = np.eye(2*circ[0],2*circ[0]+1, dtype = bool)


        for op_bloc in circ[3]:
            st = time.perf_counter()
            #We apply each bloc of gates to the tableau
            Tableau = self._Apply_gate_bloc(Tableau, op_bloc, circ)
            et = time.perf_counter()
            print(f"apply_gate_time time: {et - st} seconds")

        st = time.perf_counter()
        #we measure the observable at the end (here meas is a dict with the probability of + and -)
        meas = self._measure(Tableau, circ)
        et = time.perf_counter()
        print(f"measure time: {et - st} seconds")
        return meas


    
    def _Apply_gate_bloc(self, Tableau, dic, circ):
        for key, values in dic.items():
            # The implementation of these gate implementation is inspired by https://www.scottaaronson.com/papers/chp5.pdf

            if key == "x":
                apply_list = [value+circ[0] for value in values] + [-1]
                Tableau[:,-1] = np.sum(Tableau[:,apply_list], axis=1) % 2
            elif key == "z":
                apply_list = values + [-1]
                Tableau[:,-1] = np.logical_xor.reduce(Tableau[:,apply_list], axis=1)
            elif key == "y":
                apply_list = values + [value+circ[0] for value in values] + [-1]
                Tableau[:,-1] = np.logical_xor.reduce(Tableau[:,apply_list], axis=1) 
            elif key == "h":
                apply_list_x = values
                apply_list_z = [value+circ[0] for value in values] 
                Tableau[:,-1] = np.logical_xor.reduce((Tableau[:,apply_list_x] & Tableau[:,apply_list_z]), axis=1) ^ Tableau[:,-1]

                Tableau[:, apply_list_x + apply_list_z] = Tableau[:, apply_list_z + apply_list_x]
            elif key == "s":
                apply_list_x = values
                apply_list_z = [value+circ[0] for value in values] 
                Tableau[:,-1] = np.logical_xor.reduce((Tableau[:,apply_list_x] & Tableau[:,apply_list_z]), axis=1) ^ Tableau[:,-1]
                Tableau[:, apply_list_z] = Tableau[:, apply_list_z] ^ Tableau[:, apply_list_x]
            elif key == "cx":
                x_ctrl_q, x_trgt_q = list(zip(*values))
                z_ctrl_q, z_trgt_q = [posi + circ[0] for posi in x_ctrl_q], [posi + circ[0] for posi in x_trgt_q]

                Tableau[:,-1] = Tableau[:,-1] ^ np.logical_xor.reduce(
                    (Tableau[:,x_ctrl_q] & Tableau[:,z_trgt_q])
                    &
                    (Tableau[:,x_trgt_q] ^  Tableau[:,z_ctrl_q] ^ True)       
                    , axis=1)
                
                Tableau[:,x_trgt_q ] = Tableau[:,x_trgt_q ] ^ Tableau[:,x_ctrl_q]
                Tableau[:,z_ctrl_q ] = Tableau[:,z_trgt_q ] ^ Tableau[:,z_ctrl_q]
        return Tableau



    def _measure(self, Tableau, circ):

        # Remove the coef column \vec(r)
        stabilizers = Tableau[circ[0]:,:-1]
        # preparation of observable vector for symplectic product (x,z)->(z,x)
        anti_symp_obs = np.roll(circ[1].obs_vec, circ[0])
        # Vector of bool with information about commutation with observable
        commute_vector = np.sum(stabilizers & anti_symp_obs, axis=1) % 2

        # if one stabilizer anti-commute, for sure the obs is not measurable 
        if any(commute_vector):
            prob_0 = 1/2
        else:
            # Inverse stabilizer matrix to solve (S^T)x=Obs -> x = S^(-T)Obs
            # The sign of obs is given by the sum over \vec(x) * \vec(r)
            # print(Tableau[:,:-1])
            inv_tab = np.linalg.inv(Tableau[:,:-1].T) % 2
            sol = inv_tab @ np.transpose(circ[1].obs_vec) % 2
            # sign_ob = np.sum(Tableau[circ[0]:,-1] @ sol) % 2 
            sign_ob = np.sum(Tableau[:,-1] @ sol) % 2 
            prob_0 = int(1-sign_ob) 
        meas = {"+":prob_0, "-":(1-prob_0)}
        return meas


    def run(self, Qc):
        # n_coeurs = 8
        n_process = 8
        # result_list = []

        # create the process pool
        with Pool(n_process) as pool:
            # call function for each item in an iterable in parallel
            st = time.perf_counter()
            results = pool.map(self._Single_circ_run, Qc.struct)
            et = time.perf_counter()
            print(f"Pool time: {et - st} seconds")
        
        return results






