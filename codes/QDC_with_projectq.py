# coding: utf-8

import numpy as np
import projectq
from projectq.ops import Measure, H, X
from projectq.meta import Control

class qd_autocompresser():
    def __init__(self, data):
        self.data = data
        # input classical data, where N is the length of the data.
        self.dimension = np.log2(len(self.data))
        self.dict_V_P = {}

        # projectq
        self.eng = projectq.MainEngine()
        self.qubits = ()
        # add a auxiliary qubit:
        self.qubits += (self.eng.allocate_qubit(),)
        for i in range(int(self.dimension)):
            self.qubits += (self.eng.allocate_qubit(),)

        # the follows operation would produce a dictionary between position and the corresponding
        # massage that the position stores
        # For example:{'00': '1', '01': '0', '10': '0', '11': '0'}
        index = []
        for i in range(len(self.data)):
            if i == 0:
                index.append(1)
            else:
                for j in range(int(self.dimension)+1):
                    while i >= pow(2, j-1) and i <= pow(2, j):
                        index.append(j+1)
                        break
        for i in range(len(self.data)):
            a = bin(i)[2:2+index[i]]
            while len(a) < max(index) - 1:
                a = '0' + a
            self.dict_V_P[a] = self.data[i]

    def Control(self):
        for i in range(len(self.qubits)):
            if i != 0:
                H | self.qubits[i]

        for i in self.dict_V_P:
            if self.dict_V_P[i] == '1':
                for j in range(len(i)):
                    if i[j] == '0':
                        X | self.qubits[j + 1]
                with Control(self.eng, self.qubits[1]):
                    with Control(self.eng, self.qubits[2]):
                        X | self.qubits[0]
                for j in range(len(i)):
                    if i[j] == '0':
                        X | self.qubits[j + 1]

    def Measure(self):
        for i in range(len(self.qubits)):
            Measure | self.qubits[i]

        self.eng.flush()

        result = ''
        for qubit in self.qubits:
            result = result + str(int(qubit))
        print(result)


a = qd_autocompresser('1010')
print(a.dict_V_P)
a.Control()
a.Measure()


