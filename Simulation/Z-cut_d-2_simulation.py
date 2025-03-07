import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

no_of_qubits = 7 # 0:D1, 1:F1, 2:D2, 3:S1, 4:D3, 5:F2, 6:D4
no_of_classical_bits = 2 # 1:S1'in 1. ölçümü, 0:S1'in 2. ölçümü 

def Z_round_of_S1(cycle_no):
	# 1. adım
	circuit.reset(1)
	circuit.reset(5)
	
	# 2. adım
	circuit.cx(0, 1)
	circuit.cx(6, 5)
	
	# 3. adım
	circuit.cx(1, 2)
	circuit.reset(3)
	circuit.cx(5, 4)
	
	# 4. adım
	circuit.cx(0, 1)
	circuit.cx(2, 3)
	circuit.cx(6, 5)
	
	# 5. adım
	# F1 Z tabanında ölçülecek ama bu özelliği kullanmiycam bu programda
	circuit.reset(1)
	circuit.cx(4, 3)
	# F2 Z tabanında ölçülecek ama bu özelliği kullanmiycam bu programda
	circuit.reset(5)
	
	# 6. adım
	circuit.cx(0, 1)
	circuit.measure(3, (no_of_classical_bits - cycle_no))
	circuit.cx(6, 5)
	
	# 7. adım
	circuit.cx(1, 2)
	circuit.cx(5, 4)
	
	# 8. adım
	circuit.cx(0, 1)
	circuit.cx(6, 5)
	
	# 9. adım
	# F1 Z tabanında ölçülecek ama bu özelliği kullanmiycam bu programda
	circuit.reset(1)
	# F2 Z tabanında ölçülecek ama bu özelliği kullanmiycam bu programda
	circuit.reset(5)
	
def Apply_logical_X():
	circuit.x(6)

circuit = QuantumCircuit(no_of_qubits, no_of_classical_bits)

# Veri kübitleri başlangıçta 
# |-+++> olacak şekilde çalıştır
circuit.reset(0)
circuit.x(0)
circuit.h(0)
circuit.reset(2)
circuit.h(2)
circuit.reset(4)
circuit.h(4)
circuit.reset(6)
circuit.h(6)
circuit.barrier()

# 1. cycle
Z_round_of_S1(1)
circuit.barrier()

# Mantıksal X
Apply_logical_X()
circuit.barrier()

# 2. cycle
Z_round_of_S1(2)
circuit.barrier()

# Simulate the circuit
simulator = AerSimulator()
result = simulator.run(circuit, shots=4096).result()
counts = result.get_counts()

# Visualize the results
plot_histogram(counts)
plt.title("X applied to Fourth Data Qubit (Qubit 3)")
plt.show()

# Show circuit
circuit.draw("mpl")
plt.show()

