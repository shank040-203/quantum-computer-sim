import random
from math import log2 as log2, cos as cos, sin as sin

I = [[1, 0], [0, 1]]
X = [[0, 1], [1, 0]]  # inversion
Z = [[1, 0], [0, 1]]  # measurement
H = [[2**-0.5, 2**-0.5], [2**-0.5, -(2**-0.5)]]  # Hadamard

def operators(no_of_qubits, X_POS, Z_POS, H_POS):
    O=[[1]]
    for i in range(no_of_qubits):
        if i in X_POS:
            O=tp(X,O)
        elif i in Z_POS:
            O=tp(Z,O)
        elif i in H_POS:
            O=tp(H,O)
        else :
            O=tp(I,O)
    return O
def C_NOT(no_of_qubits, ctrl_list, ctrld_list):
    #ctrl_list is the list containing the indexes of the control qubits
    #ctrld_list is the list containing the indexex of the controlled qubits
    clen=2**(no_of_qubits)
    C=[[0 for _ in range(clen)] for __ in range(clen)]
    for i in range(clen):
        list_i = list(map(int,list(bin(i)[2:].zfill(no_of_qubits))))
        and_gate_result = 1
        for j in ctrl_list:
            and_gate_result = and_gate_result * list_i[no_of_qubits-1-j]
        if and_gate_result == 1:
            for k in ctrld_list:
                list_i[no_of_qubits-1-k] = (list_i[no_of_qubits-1-k]+1)%2
            i_dash = 0
            for k in range(no_of_qubits):
                i_dash += 2**(no_of_qubits-1-k) * list_i[k]
            C[i][i_dash] = 1
        else:
            C[i][i] = 1
    return C, clen
    
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
            fop = I
            for _ in range(i - 1):
                fop = tp(fop, I)
            fop = tp(fop, op)
        self.state = tp(fop, self.state)


def black_box(no_of_qubits,a):
    operator_position=list(bin(a)[2:].zfill(no_of_qubits))
    X_POS=[]
    for _ in operator_position:
        if _ == '0':
            X_POS.append(no_of_qubits-1-operator_position.index(_))
    O_=operators(no_of_qubits+1,X_POS,[],[])
    C, clen=C_NOT(no_of_qubits+1,list(range(no_of_qubits)),[no_of_qubits])
    O=[[0 for _ in range(clen)]for __ in range(clen)]
    for i in range(clen):
        for j in range(clen):
            for k in range(clen):
                for l in range(clen):
                    O[i][l]= O_[i][j] * C[j][k] * O_[k][l]
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
        
def grover_operator(initial_ket, no_of_qubits, a):
    S=S_operator(initial_ket)
    O=black_box(no_of_qubits,a)
    glen=2**(no_of_qubits+1)
    G=[[0 for _ in range(glen)]for __ in range(glen)]
    for i in range(glen):
        for j in range(glen):
            for k in range(glen):
                G[i][k]= S[i][j] * O[j][k]
    return G
a = [random.random() for _ in range 32]
x = random.choice(a)

s = System()
for _ in range(5):
    s.add_qubit(Qubit1())
