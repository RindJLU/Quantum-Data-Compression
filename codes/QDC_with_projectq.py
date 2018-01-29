import copy
import projectq
import numpy as np
from projectq.ops import Measure, H, X, C, All


class QImEncoder(object):
    """Store classical data/image in quantum state.

    Using Projectq, a quantum computational simulating module , to demonstrate
    information representation in qubits. First encoding classical information
    into quantum state, then retrieving information through measurement.

    Args:
        data (input)(ndarray): a array of one bit binary number where N is the length of the data.
        dimension (int): the number of qubits required to represent the data.
        numQuRep(int): the number of qubits used to represent the position
        numQuCol(int): the number of qubits used to represent the color
        posRef(ndarray): a three dimensional array,

        eng: MainEngine
        qubits:

    Returns:
        Measurement results Or Wavefunction

    """

    def __init__(self, data):
        """Initialing QImEncoder with some args."""

        self.data = data
        self.dim = self.data.shape
        self.numQuRep = int(np.log2(self.dim[0] * self.dim[1]))
        self.numQuCol = 1
        self.posRef = self._posRef()  # position reference

        """using projectq module to create qubits"""
        self.eng = projectq.MainEngine()
        self.qubits = self.eng.allocate_qureg(self.numQuCol + self.numQuRep)  # create one auxiliary qubit.

    def quStatePrep(self, cheat=True):
        """prepare quantum state for information storing"""

        All(H) | self.qubits[self.numQuCol:]  # prepare the qubits for position reference, the first(qubit[0]) remains
        # unchanged for representing corresponding value.

        for pRefRow in range(self.dim[0]):  # p_ref_index is the index of the position of the data.
            for pRefCol in range(self.dim[1]):
                if self.data[pRefRow][pRefCol] == 1:  # only the data in a position is 1, an X operation will be implemented
                    for i in range(self.numQuRep):  # reshape the qubit state to represent the corresponding position.
                        if self.posRef[pRefRow][pRefCol][i] == 0:
                            X | self.qubits[i + 1]

                    C(X, self.numQuRep) | (self.qubits[1:], self.qubits[0])  # controlled X operation to flip |0> to |1>.

                    for i in range(self.numQuRep):  # reshape the qubit to its original state
                        if self.posRef[pRefRow][pRefCol][i] == 0:
                            X | self.qubits[i + 1]

        if cheat:
            self._cheat()
        else:
            self._measure()

    def _cheat(self):

        self.eng.flush()
        mapping, wavefunction = copy.deepcopy(self.eng.backend.cheat())
        print("The full wavefunction is: {}".format(wavefunction))
        Measure | self.qubits

    def _measure(self):
        Measure | self.qubits
        self.eng.flush()

        result = ''
        for qubit in self.qubits:
            result = result + str(int(qubit))
        print('Measured {} in the position {}, {}'.format(result[0], result[1:int(np.log2(self.dim[0]))+1], result[int(np.log2(self.dim[0]))+1:]))


    def _posRef(self):
        posTemp = [[], []]
        for pos in range(len(self.dim)):
            for num in range(self.dim[pos]):
                ref_temp = bin(num)[2:]  # temporary reference
                # fun bin() would return a str head with '0b', which should be removed.
                while int(np.log2(self.dim[pos])) - len(ref_temp) != 0:  # uniform the ref repression.
                    ref_temp = '0' * (int(np.log2(self.dim[pos])) - len(
                        ref_temp)) + ref_temp  # if dim=3, then convert '0' to '000'.
                posTemp[pos].append(ref_temp)
                # posTemp has two part, one stores the binary position of row, the other stores colome.
        # print(posTemp)
        posList = []
        for row in range(len(posTemp[0])):
            for col in range(len(posTemp[1])):
                temp_list = posTemp[0][row] + posTemp[1][col]
                for i in temp_list:
                    posList.append(int(i))
        return np.array(posList).reshape([self.dim[0], self.dim[1], self.numQuRep])  # position reference

if __name__ == '__main__':
    a = QImEncoder(np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             ]))
    a.quStatePrep()

