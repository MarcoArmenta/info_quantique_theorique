# observables

import numpy as np

class PauliObservable:
    def __init__(self, Obs_string, num_q) -> None:
        self.obs_string = Obs_string


        x_part = np.zeros(num_q, dtype = bool)
        z_part = np.zeros(num_q, dtype = bool)
        for idx in range(num_q):
            if self.obs_string[idx] == "x":
                x_part[idx] = True
            elif self.obs_string[idx] == "z":
                z_part[idx] = True
            elif self.obs_string[idx] == "y":
                x_part[idx] = True
                z_part[idx] = True
            np.concatenate([x_part,z_part])

        self.obs_vec = np.concatenate([x_part,z_part])
