import random
from math import log2 as log2, cos as cos, sin as sin

I2 = [[1, 0], [0, 1]]
X = [[0, 1], [1, 0]]  # inversion
Z = [[1, 0], [0, 1]]  # measurement
H = [[2**-0.5, 2**-0.5], [2**-0.5, -(2**-0.5)]]  # Hadamard

def tp(t1, t2):
    m1, n1, m2, n2 = len(t1[0]), len(t1), len(t2[0]), len(t2)
    prod = [[0 for _ in range(m1 * m2)] for __ in range(n1 * n2)]
    for i1 in range(n1):
        for j1 in range(m1):
            for i2 in range(n2):
                for j2 in range(m2):
                    prod[i1*n2 + i2][j1*m2 + j2] = t1[i1][j1] * t2[i2][j2]
    return prod

class Qubit1:
    def __init__(self):
        self.theta = 2 * pi * random.random()
        self.p0 = cos(self.theta)
        self.p1 = sin(self.theta)
    def op(self, op):
        np0 = op[0][0] * self.p0 + op[0][1] * self.p1
        np1 = op[1][0] * self.p0 + op[1][1] * self.p1
        self.p0 = np0
        self.p1 = np1
    def __str__(self):
        p = random.random()
        if p <= self.p0 ** 2:
            return '0'
        else:
            return '1'

class System:
    def __init__(self):
        self.state = []
    def add_qubit(self, q):
        if not self.state:
            self.state = [q.p0, q.p1]
        else:
            self.state = tp(self.state, [q.p0, q.p1])
    def op_on(op, i):
        if i == 0:
            fop = op
        else:
            fop = I2
            for _ in range(i - 1):
                fop = tp(fop, I2)
            fop = tp(fop, op)
        self.state = tp(fop, self.state)


def black_box(no_of_qubits,a):
    operator_position=list(bin(a)[2:].zfill(no_of_qubits))
    O_=[[1]]
    for _ in range(no_of_qubits):
        if operator_position[no_of_qubits-_]=='0':
            O_=tp(O_,X)
        else :
            O_=tp(O_,I)
    O_=tp(O_,I)
    clen=2**(no_of_qubits+1)
    C_NOT=[[0 for _ in range(clen)]for __ in range(clen)]
    for i in range(clen-2):
        C_NOT[i][i]=1
    C_NOT[clen-1][clen-2]=1
    C_NOT[clen-2][clen-1]=1
    O=[[0 for _ in range(clen)]for __ in range(clen)]
    for i in range(clen):
        for j in range(clen):
            for k in range(clen):
                for l in range(clen):
                    O[i][l]= O_[i][j] * C_NOT[j][k] * O_[k][l]
    return O
def S_operator(initial_ket):
    l=len(initial_ket)
    S=[[0 for _ in range(l)]for __ in range(l)]
    for i in range(l):
        for j in range(l):
            if i==j:
                S[i][j] = 2 * initial_ket[i] * initial_ket[j] -1
            else :
                S[i][j] = 2 * initial_ket[i] * initial_ket[j]
    S=tp(S,I)
    return S
        
def grover_operator(initial_ket, no_of_qubits. a):
    S=S_operator(initial_ket)
    O=black_box(no_of_qubits,a)
    glen=2**(no_of_qubits+1)
    G=[[0 for _ in range(clen)]for __ in range(glen)]
    for i in range(clen):
        for j in range(clen):
            for k in range(clen):
                G[i][k]= S[i][j] * O[j][k]
    return G
a = [random.random() for _ in range 32]
x = random.choice(a)

s = System()
for _ in range(5):
    s.add_qubit(Qubit1())


