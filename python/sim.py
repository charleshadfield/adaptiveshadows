#!/usr/bin/python

import sys
import time
import multiprocessing
import numpy as np

from hamiltonian import hamiltonians
from circuits import generateBasis, runAndMeasure, buildPauliEstimates, updatePauliEstimates

def simulation(x):
    name, ground_state, n_shots_per_worker = x
    H = hamiltonians[name].SummedOp()
    pauliEstimates = buildPauliEstimates(H)
    for shot in range(n_shots_per_worker):
        basis = generateBasis(H)
        evalues = runAndMeasure(ground_state, basis)
        updatePauliEstimates(pauliEstimates, evalues, basis)
    return pauliEstimates

def stitch_simulations(H, pauliEstimatesMultiple):
    pauliEstimatesBest = {}
    for x in H:
        pauli = str(x.primitive)
        estimates = []
        for pE in pauliEstimatesMultiple:
            number = pE[pauli]['number']
            estimate = pE[pauli]['running'][-1]
            estimates.append((number, estimate))
        pauliEstimatesBest[pauli] = _stitch_estimates(estimates)
    return pauliEstimatesBest

def _stitch_estimates(estimates):
    number_total = sum(estimates[i][0] for i in range(len(estimates)))
    if number_total == 0:
        estimate = 0.0
    else:
        estimate = 1/number_total * sum(np.prod(estimates[i]) for i in range(len(estimates)))
    return estimate

def energyEstimate(H, pauliEstimatesBest):
    energyRunning = 0.0
    for x in H:
        coeff, pauli = x.coeff, str(x.primitive)
        energyRunning += coeff * pauliEstimatesBest[pauli]
    return energyRunning


def main():
    ### Preparation
    name = sys.argv[1]
    assert name in hamiltonians, "Molecule not recognized."
    ham = hamiltonians[name]
    print("Molecule is {} in {} encoding.".format(name.split('_')[0],name.split('_')[1]))
    n_shots = 1000
    print("Number of shots is set to {}.".format(n_shots))

    ### Ground information
    print("Calculating ground energy and ground state...")
    t0 = time.time()
    ground_energy, ground_state = ham.ground(sparse=True)
    t1 = time.time()
    diff = int(t1-t0)
    print("Done\nGround information calculated in {}min{}sec.".format(diff // 60, diff % 60))

    ### Simulation
    n_workers = 15
    n_shots_per_worker = int(np.ceil(n_shots / n_workers))
    #assert n_workers * n_shots_per_worker == n_shots, "Your math doesn't check out!"

    print("Pooling {} workers to simulate roughly {} shots each...".format(n_workers, n_shots_per_worker))
    t0 = time.time()
    p = multiprocessing.Pool(n_workers)
    x = (name, ground_state, n_shots_per_worker)
    y = (name, ground_state, n_shots - (n_workers-1)*n_shots_per_worker)
    inputs = [x for _ in range(n_workers-1)]
    inputs.append(y)
    outputs = p.map(simulation, inputs)
    t1 = time.time()
    diff = int(t1-t0)
    print("Done\nPooling took {}min{}sec.".format(diff // 60, diff % 60))

    ### Return energy estimate
    H = ham.SummedOp()
    pauliEstimatesMultiple = outputs
    pauliEstimatesBest = stitch_simulations(H, pauliEstimatesMultiple)
    estimate = energyEstimate(H, pauliEstimatesBest)

    print('true       :', ground_energy)
    print('estimate   :', estimate)
    print('difference :', estimate - ground_energy)

if __name__ == "__main__":
    main()
