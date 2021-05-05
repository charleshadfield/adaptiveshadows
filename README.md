# adaptiveshadows
Locally-biased classical shadows with an adaptive update

## How do we generate a measurement basis?

### One qubit at a time update idea

Consider $H = \sum_P \alpha_P P$ on $n$ qubits. Set $\mathcal{B}=\{X,Y,Z\}$.

Let $i:[n]\to[n]$ be a bijection randomly chosen from all possible bijections. This gives an ordering of the qubits $i(1), \dots, i(n)$. Write $i(j)$ for $j\in[n]$.

We will chose $\beta_{i(j)}:\mathcal{B}\to\mathbb{R}^+$ in an adaptive style.

Let's do this slowly:

- $j=1$.
    - Set $A = \{ P \in H | P_{i(1)} \in \mathcal{B} \}$.
    - Minimise $\Delta(\beta_{i(1)}) = \sum_{P\in A} \alpha_P^2 / \beta_{i(1)}(P_{i(1)})$.
    - Pick $B_{i(1)}$ from $\beta_{i(1)}$.
- $j>1$.
    - Set $A = \{ P \in H | P_{i(j)} \in \mathcal{B} \textrm{ and for all $j'<j$ } P_{i(j')} \in \{I, B_{i(j')}\} \}$.
    - Minimise $\Delta(\beta_{i(j)}) = \sum_{P\in A} \alpha_P^2 / \beta_{i(j)}(P_{i(j)})$.
    - Pick $B_{i(1)}$ from $\beta_{i(1)}$.

Now set $B = \otimes_{i\in[n]} B_i$

Actually, it is even easier because the minimisation procedure can be done analytically. Given $j$ and $A$ do the following:
- Set $A = A_X + A_Y + A_Z$ where $A_B = { P\in A | P_{i(j)}=B }$
- Set $c_B = \sum_{P \in A_B} \alpha_P^2$
- Set $c = \sum_B \sqrt{c_B}$
- Set $\beta_{i(j)}(B) = \sqrt{c_B} / c$

## Current results:

Take a Hamiltonian, and allow access to the ground state 1000 times. Record the energy difference between the estimated energy and the true ground energy.

| Molecule | Encoding | Derand | Adaptive                                         | time(diag) | time(estimate) |
|----------|----------|--------|--------------------------------------------------|------------|----------------|
| H2       | JW       | 0.06   | 0.003, 0.04, 0.08, 0.09, 0.12, 0.15, 0.09, 0.004 | 1sec       | 10sec          |
| LiH      | JW       | 0.03   | 0.01, 0.07, 0.03                                 | 1sec       | 2min30         |
|          |          |        |                                                  |            |                |
