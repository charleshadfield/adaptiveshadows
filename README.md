# adaptiveshadows
Locally-biased classical shadows with an adaptive update

## How do I run this?

Install requirements, and navigate to folder `adaptiveshadows/python`. Then call `python sim.py <name>` where `<name>` is the molecule and encoding joined by an underscore. Molecules are: `h2, lih, beh2, h2o, nh3` and encodings are `jw, parity, bk`. So one example of `<name>` is `h2_jw`.

## Current results:

Take a Hamiltonian, and allow access to the ground state 1000 times. Record the energy difference between the estimated energy and the true ground energy.

| Molecule | Encoding | Derand | Adaptive                                                           | Adaptive RSME | Diagonalize | Simulation |
|----------|----------|--------|--------------------------------------------------------------------|---------------|-------------|------------|
| H2       | JW       | 0.06   | 0.003, 0.04, 0.08, 0.09, 0.12, 0.15, 0.09, 0.004, 0.08, 0.03, 0.046| 0.08          | 1sec        | 10sec      |
|          | Parity   | 0.03   | 0.02, 0.047, 0.054, 0.058, 0.036, 0.085, 0.029, 0.031, 0.01, 0.053 | 0.05          |             |            |
|          | BK       | 0.06   | 0.12, 0.03, 0.01, 0.03, 0.05, 0.04, 0.01, 0.02, 0.017, 0.2         | 0.08          |             |            |
| LiH      | JW       | 0.03   | 0.07, 0.027, 0.07, 0.01, 0.05, 0.02, 0.03, 0.04, 0.06, 0.02, 0.04  | 0.04          | 1sec        | 1min50sec  |
|          | Parity   | 0.03   | 0.01, 0.05, 0.07, 0.01, 0.05, 0.07, 0.03, 0.04, 0.03, 0.05         | 0.05          |             | 1min30sec  |
|          | BK       | 0.04   | 0.02,  0.009, 0.1, 0.09, 0.06, 0.1, 0.008, 0.1, 0.02, 0.02         | 0.07          |             | 1min40sec  |
| BeH2     | JW       | 0.06   | 0.02, 0.057, 0.05, 0.07, 0.06, 0.04, 0.055, 0.07, 0.07, 0.11       | 0.06          | 7sec        | 6min20sec  |
|          | Parity   | 0.09   | 0.09, 0.051, 0.06, 0.06, 0.05, 0.05, 0.07, 0.06, 0.1, 0.0009       | 0.06          |             | 5min40sec  |
|          | BK       | 0.06   | 0.07, 0.06, 0.05, 0.05, 0.08, 0.07, 0.06, 0.07, 0.07, 0.06         | 0.06          |             | 6min       |
| H2O      | JW       | 0.12   | 0.12, 0.12, 0.13, 0.1, 0.1, 0.12, 0.10, 0.09, 0.09, 0.1            | 0.11          | 15sec       | 6min45sec  |
|          | Parity   | 0.22   | 0.16, 0.056, 0.12, 0.1, 0.12, 0.1, 0.12, 0.09, 0.11, 0.09, 0.11    | 0.11          |             | 6min10sec  |
|          | BK       | 0.20   | 0.028, 0.11, 0.11, 0.1, 0.11, 0.09, 0.12, 0.11, 0.1, 0.11          | 0.10          |             | 6min10sec  |
| NH3      | JW       | 0.18   | 0.11, 0.076, 0.0507, 0.12, 0.14, 0.18, 0.16, 0.14, 0.14, 0.14      | 0.13          | 5min30      | 28min      |
|          | Parity   | 0.21   | 0.079, 0.086, 0.17, 0.14, 0.14, 0.14, 0.18, 0.15, 0.16, 0.16       | 0.14          |             | 26min      |
|          | BK       | 0.12   | 0.06, 0.09, 0.13, 0.13, 0.13, 0.14, 0.06, 0.15, 0.03, 0.10         | 0.11          |             | 27min      |

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
