from qiskit.quantum_info import Pauli
from qiskit.aqua.operators import PauliOp, SummedOp

def isCompatible(P: Pauli, B: list, j: int) -> bool:
    for i in range(j):
        assert B[i] in ('X', 'Y', 'Z'), "Qubits before j={} need an X,Y,Z basis.".format(j)
        if P.to_label()[i] not in ('I', B[i]):
            return False
    return True

def zeta(P: Pauli, beta: list) -> float:
    zeta_running = 1.0
    for i in range(P.num_qubits):
        Pi = P.to_label()[i] # i^th Pauli is I,X,Y,or Z
        if Pi != 'I':
            index = {'X': 0, 'Y': 1, 'Z': 2}[Pi]
            zeta_running *= beta[i][index]
    return zeta_running

def cost(H: SummedOp, beta: list, B: list, j: int) -> float:
    cost_running = 0.0
    for pauliOp in H:
        P, coeff_P = pauliOp.primitive, pauliOp.coeff
        if isCompatible(P, B, j):
            cost_running += coeff_P**2 / zeta(P, beta)
    return cost_running
