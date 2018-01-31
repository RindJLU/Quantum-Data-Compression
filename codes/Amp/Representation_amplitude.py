import copy
import projectq
from projectq.ops import H, X, All, Measure
import numpy as np


class AmpRep(object):
    """
    This is another data representation approach. Here the data was stored as the amplitude of qubits. For example, the
    data [1, 1, 1, 1] can be represented as 0.5(1*|00> + 1*|01> +  1*|10> +  1*|11>). The method to store information
    into quantum state in this way is difficult. Thus using MainEngine().backend.set_wavefunction() to set corresponding
    wave function.

    Input:
        data(ndarray): the

    Args:
        data(ndarray)
        dim():
        numQuRep(int):

        eng():
        qureg():

    Returns:


    """
    def __init__(self, data, set_wave_fun=True):
        self.data = self._norm(data)
        self.dim = self.data.shape
        self.numQuRep = int(np.log2(self.dim[0] * self.dim[1]))

        """using projectq module to create qubits"""
        self.eng = projectq.MainEngine()
        self.qureg = self.eng.allocate_qureg(self.numQuRep)

        if set_wave_fun:
            self.eng.flush()
            self.eng.backend.set_wavefunction(self.data.reshape(self.dim[0] * self.dim[1]).tolist(), self.qureg)
        self._ms()

    def _ms(self, set_wave_fun=True):
        if not set_wave_fun:
            self.eng.flush()
        mapping, wave_function = copy.deepcopy(self.eng.backend.cheat())
        print('The wave_function of the system is {}'.format(wave_function))
        Measure | self.qureg

    def _norm(self, data):
        sq_sum = sum(data.real*data.real + data.imag * data.imag)
        np.seterr(divide='ignore', invalid='ignore')
        norm_data = data/sq_sum
        return norm_data


if __name__ == '__main__':
    a = AmpRep(np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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

