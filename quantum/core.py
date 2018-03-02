import enum
from itertools import product
from math import log
import random
from contextlib import contextmanager
import numpy as np


class Result(enum.Enum):
    Zero = 0
    One  = 1


class QuantumSystem:
    def __init__(self):
        self.bits = 0
        self.state = np.zeros([2] * self.bits, dtype="complex")
        self.state.flat[0] = 1.0 + 0.0j

    @contextmanager
    def register(self, n):
        qubits = []
        for i in range(n):
            tmp = np.zeros_like(self.state)
            self.state = np.stack([self.state, tmp], axis=-1)
            qubits.append(Qubit(self.bits + i))
        self.bits += n

        yield qubits

        slices = [slice(None) for _ in range(self.bits)]
        for i in range(n):
            slices[-1-i] = 0
        prob = (abs(self.state.__getitem__(tuple(slices))) ** 2).sum()
        if abs(prob - 1) > 1e-6:
            raise RuntimeError("You must set the qubits to Zero before releasing them.\nProb:{}".format(prob))
        self.state = self.state.__getitem__(tuple(slices)) / prob ** 0.5
        self.bits -= n
        for qubit in qubits:
            qubit.release()

    def apply_operator(self, matrix, qubits):
        for qubit in qubits:
            if qubit.is_released():
                raise RuntimeError("Operation on released qubit is not allowed.")
        indices = [qubit.index for qubit in qubits]
        dims = list(range(self.bits))
        for i, dim in enumerate(indices):
            dims[dim], dims[i] = dims[i], dims[dim]
        state = self.state.transpose(*dims).reshape(-1, int(2**len(dims[:-len(indices)])))
        state = np.array(np.matmul(matrix, state))
        shape = [2] * self.bits
        state = state.reshape(*shape)
        self.state = state.transpose(*dims)
        amp = (self.state ** 2).sum() ** 0.5
        self.state /= amp

    def measure(self, qbit):
        slices = [slice(None) for _ in range(self.bits)]
        slices[qbit.index] = 1
        prob = (abs(self.state.__getitem__(tuple(slices))) ** 2).sum()
        result = Result.One if random.random() <= prob else Result.Zero
        self._collapse(qbit, result)
        return result

    def _collapse(self, qbit, result):
        # Collapse (one bit of) the system to a given result
        slices = [slice(None) for _ in range(self.bits)]
        slices[qbit.index] = 1 if result == Result.Zero else 0
        prob = (abs(self.state.__getitem__(tuple(slices))) ** 2).sum()
        self.state.__setitem__(tuple(slices), 0)
        self.state /= (1 - prob) ** 0.5

    @property
    def num_states(self):
        return int(2**self.bits)

    def __getitem__(self, i):
        if i >= self.bits or i < 0:
            raise ValueError
        return Qubit(i)

    def __repr__(self):
        text = []
        length = self.bits
        fmt = "|{:0>%d}>" % length
        for i, amp in enumerate(self.state.flat):
            if abs(amp) ** 2 < 1e-5:
                continue
            state = fmt.format(bin(i)[2:])
            text.append("\t{}\t|\t{:.3f}".format(state, amp))
        return "\n".join(text)


class Qubit:
    def __init__(self, index):
        self.index = index
        self._released = False

    def release(self):
        self._released = True

    def is_released(self):
        return self._released


__system = None
def get_system(bits=10):
    global __system
    if not __system:
        __system = QuantumSystem()
    return __system

