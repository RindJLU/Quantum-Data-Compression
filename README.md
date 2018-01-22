# Quantum-Data-Compression

###1. Introduction.
Quantum data compression, in which the data could be a list of number, a picture, or a video. The target of quantum data
 compression is to find a feasible way to encode classical data into quantum state. Such encoding options can be vary. 
Take the representation of pictures as an example, many quantum image representation(QImR) has been discussed as follows.

[A Survey of Quantum Image Representations]https://doi.org/10.1007/s11128-015-1195-6\
[Processing and Retrieving an Image Using Quantum Mechanics]https://doi.org/10.1117/12.485960\
[A Novel Enhanced Quantum Representation of Digital Images]https://doi.org/10.1007/s11128-013-0567-z\
[A Flexible Representation of Quantum Images for Polynomial Preparation, Image Compression, and Processing Operations]
https://doi.org/10.1007/s11128-010-0177-y

The following discussion is based on the paper [[A Flexible Representation of Quantum Images for Polynomial Preparation, Image Compression, and Processing Operations]].

###2. Quantum image representation.
####2.1 Brief Introduction of QImR.
A classical image which sized 2^n * 2^n in terms of pixel can be stored in only 1 + 2n qubits, where the first qubit used 
to control the color information, while the other 2n qubit stores the corresponding position of the image.

Thus a coded qubits having the wavefunction:  I(θ) = (cos θ i |0> + sin θ i |1>) ⊗ |i>.

For every position, which has its index i, the corresponding color was stored in θ. To achieve this, a straightforward way 
is to control every position individually. In this way, a totally 2^n * 2^n nqubits controlled gates are required. Since 
nqubits gate requires exponential single and CNot gates, the total gates required for the encoding quantum circuits would
 expand exponentially. Thus, it is not efficient to implement such method.
 
####2.2 Improved QImR.


####2.3 Example of improved QImR.
A 2 * 2 image, which 



###3. Quantum Data Storing: a dimension-reduced application of QImR.
Suppose we storing a list of data instead of a picture, the main difference is that the former has less color dimension.
A binary number has only two 'colors', black and white. This greatly simplifies the quantum representation of binary number,
as well as the quantum circuits design. Suppose there is a four bit classical number, say 0101, the representation procedure
 is listed as follows.
 
To store a number with 2^1 * 2^1 bits, we could use 1 + 2*1 qubits to store it. In the first place, create three qubits
with initial state |0>. Next, to the qubits which represent the position of the data, implementing a Hamiltonian operation.
After that, the 2 qubits have a wavefunction (1/2)(|00> +　|01>　+ |10> + |11>), four component represent four positions
of the binary number. The following is to control the bit representing the 'color' using control gate. For our example, the
first bit is linked to the position |00>, and it has the 'color' 0, so implementing C(I, 2), where I is the unit matrix, and 
this operation equals no operation. For the second, using |01> to represent its position, and implementing C(X, 2), where the
flip the 'color' index from |0> to |1>. The same for other positions.

By doing those operations, the final wavefunction becomes (1/2)(|0>⊗|00> + |1>⊗|01> + |0>⊗|10> + |1>⊗|11>). To extract 
message from the wavefunction, first measuring the position part, and then the 'color' part.

