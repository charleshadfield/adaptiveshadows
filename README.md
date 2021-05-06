# adaptiveshadows
Locally-biased classical shadows with an adaptive update

## How do I run this?

Install requirements, and navigate to folder `adaptiveshadows/python`. Then call `python sim.py <name>` where `<name>` is the molecule and encoding joined by an underscore. Molecules are: `h2, lih, beh2, h2o, nh3` and encodings are `jw, parity, bk`. So one example of `<name>` is `h2_jw`.

## Current results:

Take a Hamiltonian, and allow access to the ground state 1000 times. Record the energy difference between the estimated energy and the true ground energy.

| Molecule | Encoding | Derand | Adaptive                                         | Diagonalize | Simulation |
|----------|----------|--------|--------------------------------------------------|-------------|------------|
| H2       | JW       | 0.06   | 0.003, 0.04, 0.08, 0.09, 0.12, 0.15, 0.09, 0.004 | 1sec        | 10sec      |
|          | Parity   | 0.03   | 0.02                                             |             |            |
|          | BK       | 0.06   | 0.12, 0.03                                       |             |            |
| LiH      | JW       | 0.03   | 0.07                                             | 1sec        | 1min50sec  |
|          | Parity   | 0.03   | 0.01                                             |             | 1min30sec  |
|          | BK       | 0.04   | 0.15                                             |             |            |
| BeH2     | JW       | 0.06   | 0.02                                             | 7sec        | 6min20sec  |
|          | Parity   | 0.09   | 0.09                                             |             | 5min40sec  |
|          | BK       | 0.06   | 0.12                                             |             | 6min04sec  |
| H2O      | JW       | 0.12   |                                                  | 15sec       |            |
|          | Parity   | 0.22   |                                                  |             |            |
|          | BK       | 0.20   |                                                  |             |            |
| NH3      | JW       | 0.018  |                                                  | 5min30      |            |
|          | Parity   | 0.21   |                                                  |             |            |
|          | BK       | 0.12   |                                                  |             |            |


## How do we generate a measurement basis?

### One qubit at a time update idea

Consider $H = \sum_P \alpha_P P$ on $n$ qubits. Set $\mathcal{B}=\{X,Y,Z\}$.

Let $i:[n]\to[n]$ be a random bijection. This gives an ordering of the qubits $i(1), \dots, i(n)$. Write $i(j)$ for $j\in[n]$.

We will chose $\beta_{i(j)}:\mathcal{B}\to\mathbb{R}^+$ in an adaptive style.

Let's do this slowly:

- $j=1$.
    - Set $A = \{ P \in H | P_{i(1)} \in \mathcal{B} \}$.
    - Minimise $\Delta(\beta_{i(1)}) = \sum_{P\in A} \alpha_P^2 / \beta_{i(1)}(P_{i(1)})$.
    - Pick $B_{i(1)}$ from $\beta_{i(1)}$.
- $j>1$.
    - Set $A = \{ P \in H | P_{i(j)} \in \mathcal{B} \textrm{ and } P_{i(j')} \in \{I, B_{i(j')}\} \textrm{ for } j'<j \}$.
    - Minimise $\Delta(\beta_{i(j)}) = \sum_{P\in A} \alpha_P^2 / \beta_{i(j)}(P_{i(j)})$.
    - Pick $B_{i(j)}$ from $\beta_{i(j)}$.

Now set $B = \otimes_{i\in[n]} B_i$

Actually, the minimisation procedure can be done analytically. Given $j$ and $A$ do the following:
- Set $A = A_X \cup A_Y \cup A_Z$ where $A_B = \{ P\in A | P_{i(j)}=B \}$
- Set $c_B = \sum_{P \in A_B} \alpha_P^2$
- Set $c = \sum_B \sqrt{c_B}$
- If $c=0$ set $\beta_{i(j)}(B)=1/3$ else set $\beta_{i(j)}(B) = \sqrt{c_B} / c$
