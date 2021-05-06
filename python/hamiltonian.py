import itertools
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

from qiskit.quantum_info import Pauli
from qiskit.opflow import PauliOp, SummedOp

def read_encoding_return_dict(path):
    with open(path, 'r') as f:
        first_line = f.readline()
        first_character = first_line[0]
        if first_character == '{':
            format = 'dictionary'
        else:
            format = 'list'

    if format == 'dictionary':
        dic = {}
        with open(path, 'r') as f:
            dict1 = eval(f.read())
            list2 = dict1['paulis']
            for item in list2:
                pauli_string = item['label']
                coeff = item['coeff']['real']
                dic[pauli_string] = coeff
        return dic

    if format == 'list':
        dic = {}
        with open(path, 'r') as f:
            for line1, line2 in itertools.zip_longest(*[f]*2):
                pauli_string = line1[:-1]
                coefficient = float(line2[1:-5])
                dic[pauli_string] = coefficient
        return dic

    pass

class Hamiltonian():

    def __init__(self, folder, encoding):
        self.folder = folder
        self.encoding = encoding
        self.path = self.path()
        #self.pauli_rep = PauliRep(self._pauli_rep_dic())
        #self.num_qubits = self.pauli_rep.num_qubits

    def path(self):
        path = '../Hamiltonians/{0}/{1}.txt'.format(self.folder, self.encoding)
        return path

    def SummedOp(self):
        dictionary = read_encoding_return_dict(self.path)
        paulis = []
        for P, coeff_P in dictionary.items():
            paulis.append(coeff_P * PauliOp(Pauli.from_label(P)))
        return SummedOp(paulis)

    def ground(self, sparse=False):
        if not sparse:
            mat = self.SummedOp().to_matrix()
            evalues, evectors = np.linalg.eigh(mat)
        else:
            mat = self.SummedOp().to_spmatrix()
            evalues, evectors = eigsh(mat, which='SA')
            # SA looks for algebraically small evalues
        index = np.argmin(evalues)
        ground_energy = evalues[index]
        ground_state = evectors[:,index]
        return ground_energy, ground_state

# 4 qubits
h2_jw_4 = Hamiltonian('H2_STO3g_4qubits', 'jw')
h2_parity_4 = Hamiltonian('H2_STO3g_4qubits', 'parity')
h2_bk_4 = Hamiltonian('H2_STO3g_4qubits', 'bk')

# 8 qubits
h2_jw = Hamiltonian('H2_6-31G_8qubits', 'jw')
h2_parity = Hamiltonian('H2_6-31G_8qubits', 'parity')
h2_bk = Hamiltonian('H2_6-31G_8qubits', 'bk')

# 12 qubits
lih_jw = Hamiltonian('LiH_STO3g_12qubits', 'jw')
lih_parity = Hamiltonian('LiH_STO3g_12qubits', 'parity')
lih_bk = Hamiltonian('LiH_STO3g_12qubits', 'bk')

# 14 qubits
beh2_jw = Hamiltonian('BeH2_STO3g_14qubits', 'jw')
beh2_parity = Hamiltonian('BeH2_STO3g_14qubits', 'parity')
beh2_bk = Hamiltonian('BeH2_STO3g_14qubits', 'bk')

h2o_jw = Hamiltonian('H2O_STO3g_14qubits', 'jw')
h2o_parity = Hamiltonian('H2O_STO3g_14qubits', 'parity')
h2o_bk = Hamiltonian('H2O_STO3g_14qubits', 'bk')

# 16 qubits
nh3_jw = Hamiltonian('NH3_STO3g_16qubits', 'jw')
nh3_parity = Hamiltonian('NH3_STO3g_16qubits', 'parity')
nh3_bk = Hamiltonian('NH3_STO3g_16qubits', 'bk')


hamiltonians = {"h2_jw": h2_jw,
                "h2_parity": h2_parity,
                "h2_bk": h2_bk,
                "lih_jw": lih_jw,
                "lih_parity": lih_parity,
                "lih_bk": lih_bk,
                "beh2_jw": beh2_jw,
                "beh2_parity": beh2_parity,
                "beh2_bk": beh2_bk,
                "h2o_jw": h2o_jw,
                "h2o_parity": h2o_parity,
                "h2o_bk": h2o_bk,
                "nh3_jw": nh3_jw,
                "nh3_parity": nh3_parity,
                "nh3_bk": nh3_bk}
