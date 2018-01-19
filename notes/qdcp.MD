#Quantum Data Compressing
## 1. Basic Principle
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>
To understand how can we compress classical data into quantum data, let's look at the following example.\
Say, there are four bits data, representing by four classical bits, 
These data can be represented by qubit, we could use 



###Papers
####1. A flexible representation of quantum images for polynomial preparation, image compression, and processing operations
__KEY__: Flexible Representation of Quantum Images (FRQI), A __constructive polynomial preparation__ for the FRQI state from an initial
state, an algorithm for quantum image compression (QIC), and processing operations
for quantum images are combined to build the whole process for quantum image processing on FRQI.

Methods of Storing Information: divided into two parts, the first part store the position, and the second 
store the information, here the information is the color, which is represented by theta(continuous and discreet).

Inspiring: to store only the 2-bits classical information, using discreet representation, only black and white(0 and 1).

The trick to reduce the computational resources is __quantum information compression__, which reduce the quantum 
gate used in the state preparation by minimizing the Boolean expression. On the one hand, it reduces the required gates, on the 
other hand, the complexity of controlled gate is reduced.

__Karnaugh map__

####2. Quantum autoencoders for efficient compression of quantum data
__KEY__:Compressing data set x to low dimensional data set y, from where x could be recovered. This just like classical 
neural network, where high dimensional data could be represented by low dimensional parameters. For example, to store a linear 
data, it is useful to store only two parameters, a and b. Thus every data can be represented as y = a*x + b. 

Graphical representation: Two parts, encoder and decoder. Encoder compress high dimensional data into lower dimension, and decoder
 can give the result under the input qubits. Take its classical counterpart as an example, compress many data into a function,
 and return a value under a give x, the similarity between the value and y reflects the fidelity of the model.
 
The author come up with two programmable circuits, which requires O(n^2) gates. Training model can be seen in Figure 4.


####3. Quantum Data Compression(a report)
#####Lossless Quantum Data Compression Scheme:(by Kim Bostrom and Timo Felbinger)\
A mapping from source space to code space.(Based on density operator)

__1. Extension-Brute Force__

__2. Improved BF Algorithm__

__3. Adapted Algorithm__


####4.Quantum	data	compression, quantum information	generation,	and	the	density-matrix renormalization	group method.
__KEY:__ Density-marix renormalization group(DMRG).

References:
1. B. Schumacher, Phys. Rev. A 51, 2738 (1995).\
Compresses message to a smaller Hilbert space without compromising the fidelity of the message for N → ∞.

####5. Quantum Data Compression of a Qubit Ensemble

