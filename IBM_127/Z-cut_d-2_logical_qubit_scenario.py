from qiskit import QuantumCircuit, transpile
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import matplotlib.pyplot as plt
import numpy as np
import random as rd

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

'''#QiskitRuntimeService.save_account(channel="ibm_quantum", token="ce340ef9fb79c9cfdd0b11d248999856a54fbceb7be04687a4ec4287440327a86fd83edcc398b15ee5b361936c6f284c4fd1c03ec9227b11ee2d920751abde25", overwrite=True, set_as_default=True) 
service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

circuit = QuantumCircuit(no_of_qubits, no_of_classical_bits)

# Veri kübitlerini rastgele pozisyonlara getir
# Kutuplara yakın olsun
#circuit.rx(np.pi/rd.randint(6, 18), 0)
#circuit.rz(np.pi/rd.randint(6, 18), 0)
#if rd.randint(0, 1) == 1:
#	circuit.x(0)
#circuit.rx(np.pi/rd.randint(6, 18), 2)
#circuit.rz(np.pi/rd.randint(6, 18), 2)
#if rd.randint(0, 1) == 1:
#	circuit.x(2)
#circuit.rx(np.pi/rd.randint(6, 18), 4)
#circuit.rz(np.pi/rd.randint(6, 18), 4)
#if rd.randint(0, 1) == 1:
#	circuit.x(4)
#circuit.rx(np.pi/rd.randint(6, 18), 6)
#circuit.rz(np.pi/rd.randint(6, 18), 6)
#if rd.randint(0, 1) == 1:
#	circuit.x(6)
#circuit.barrier()

# Tüm veri kübitleri başlangıçta 
# |+> olacak şekilde çalıştır
circuit.reset(0)
circuit.h(0)
circuit.reset(2)
circuit.h(2)
circuit.reset(4)
circuit.h(4)
circuit.reset(6)
circuit.h(6)

# 1. cycle
Z_round_of_S1(1)
circuit.barrier()

# Mantıksal X
Apply_logical_X()
circuit.barrier()

# 2. cycle
Z_round_of_S1(2)
circuit.barrier()

#circuit.draw("mpl") 
#plt.show()

# Developer qubit A → Physical qubit B
layout = {circuit.qubits[0]: 39, circuit.qubits[1]: 40, circuit.qubits[2]: 41, circuit.qubits[3]: 53, circuit.qubits[4]: 60, circuit.qubits[5]: 59, circuit.qubits[6]: 58} 
transpiled_circuit = transpile(circuit, backend, initial_layout=layout)
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(transpiled_circuit)
sampler = Sampler(backend)
job = sampler.run([isa_circuit]) # Default 4096 shot'''

# Son klasik bit counts'ta solda
# Bu kısım biten işlemin sonuçlarını görmek için
service = QiskitRuntimeService()
job = service.job('cz4rqdd39f40008sdw00')
job_result = job.result()
# To get counts for a particular pub result, use 
#
pub_result = job_result[0].data.c.get_counts()
print(pub_result)
#
# where <idx> is the index of the pub and <classical register> is the name of the classical register. 
# You can use circuit.cregs to find the name of the classical registers.













