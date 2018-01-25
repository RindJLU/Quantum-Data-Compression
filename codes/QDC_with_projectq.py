import numpy as np
import projectq
from projectq.ops import Measure, H, X, C, All


class QImEncoder(object):
    """Store classical data/image in quantum state.

    Using Projectq, a quantum computational simulating module , to demonstrate
    information representation in qubits. First encoding classical information
    into quantum state, then retrieving information through measurement.

    Args:
        data (ndarray): a array of one bit binary number where N is the length of the data.
        dimension (int): the number of qubits required to represent the data.

        eng:
        qubits:

    Returns:


    """

    def __init__(self, data):
        """Initialing QImEncoder with some args."""

        self.data = data
        self.posRef = []  # position reference
        self.dimension = int(np.ceil(np.log2((len(self.data)))))
        for num in range(len(data)):
            ref_temp = bin(num)[2:]  # temporary reference
            # fun bin() would return a str head with '0b', which should be removed.
            while self.dimension - len(ref_temp) != 0:  # uniform the ref repression.
                ref_temp = '0' * (self.dimension - len(ref_temp)) + ref_temp  # if dim=3, then convert '0' to '000'.
            self.posRef.append(ref_temp)

        """using projectq module to create qubits"""
        self.eng = projectq.MainEngine()
        self.qubits = self.eng.allocate_qureg(self.dimension + 1)  # create one auxiliary qubit.

    def quStatePrep(self, cheat=False):
        """prepare quantum state for information storing"""

        All(H) | self.qubits[1:]# prepare the qubits for position reference, the first(qubit[0]) remains
        # unchanged for representing corresponding value.

        for p_ref_index in range(len(self.data)):  # p_ref_index is the index of the position of the data.
            while self.data[p_ref_index] == 1: # only the data in a position is 1, an X operation will be implemented.
                for i in self.dimension:  # reshape the qubit to represent the corresponding position.
                    if self.posRef[p_ref_index][i] == 1:
                        X | qubits[i]

                C(X, self.dimension) | (self.qubits[1:], self.qubits[0])  # controlled X operation to flip |0> to |1>.

                for i in self.dimension:  # reshape the qubit to its original state
                    if self.posRef[p_ref_index][i] == 1:
                        X | qubits[i]

        if cheat:
            self._cheat()
        else:
            self._measure()

    def _cheat(self):

        self.eng.flush()
        order, vec = self.eng.backend.cheat()

        Measure | self.qubits

        result = ''
        for qubit in self.qubits:
            result = result + str(int(qubit))
        print('Measured {} in the position {}'.format(result[0], result[1:]))

    def _measure(self):
        Measure | self.qubits

        self.eng.flush()

        result = ''
        for qubit in self.qubits:
            result = result + str(int(qubit))
        print('Measured {} in the position {}'.format(result[0], result[1:]))

if __name__ == '__main__':
    a = QImEncoder('1010')
    print(type(a.qubits[0]))
    a.quStatePrep()
