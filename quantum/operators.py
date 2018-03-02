from math import log
import random
import numpy as np
from scipy.linalg import block_diag
from .core import get_system, Result


class MatrixOperation:
    def __init__(self, matrix, unitary=True):
        if unitary:
            self._assert_unitary(matrix)
        self.matrix = matrix
        self.unitary = unitary
        
    @staticmethod
    def _assert_unitary(matrix):
        adjoint = matrix.getH()
        m = matrix * adjoint
        assert np.allclose(m - np.eye(m.shape[0]), np.zeros_like(m)), "The matrix is not unitary"
            
    def __call__(self, *args):
        nvars = int(log(max(self.matrix.shape)) / log(2))
        if len(args) != nvars:
            assert TypeError("Number of parameters not match")
        system = get_system()
        system.apply_operator(self.matrix, args)

    def adjoint(self):
        return MatrixOperation(self.matrix.getH(), self.unitary)

    def controlled(self):
        return MatrixOperation(np.matrix(block_diag(np.eye(self.matrix.shape[0]), self.matrix)))


# Identity
I = MatrixOperation(np.matrix(np.eye(2, dtype="complex")))


# Harmard
H = MatrixOperation(0.5**0.5 * np.matrix([[1, 1], [1, -1]], dtype="complex"))


# Pauli X
X = MatrixOperation(np.matrix([[0, 1], [1, 0]], dtype="complex"))


# Pauli Y
Y = MatrixOperation(np.matrix([[0, -1j], [1j, 0]], dtype="complex"))


# Pauli Z
Z = MatrixOperation(np.matrix([[1, 0], [0, -1]], dtype="complex"))


Swap = MatrixOperation(np.matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype="complex"))


# Phase shifter
def Phase(theta):
    return MatrixOperation(np.matrix([[1, 0], [0, np.exp(theta*1j)]], dtype="complex"))


# Controlled not
# CNot = MatrixOperation(np.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype="complex"))
CNot = X.controlled()


Toffoli = CNot.controlled()


def Measure(qbit):
    system = get_system()
    return system.measure(qbit)

def Set(qbit, desire):
    result = Measure(qbit)
    if result != desire:
        X(qbit)

def Reset(qbit):
    Set(qbit, Result.Zero)

def ResetAll(qbits):
    for qbit in qbits:
        Reset(qbit)

