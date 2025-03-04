from qiskit import QuantumCircuit, transpile
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import matplotlib.pyplot as plt

#QiskitRuntimeService.save_account(channel="ibm_quantum", token="ce340ef9fb79c9cfdd0b11d248999856a54fbceb7be04687a4ec4287440327a86fd83edcc398b15ee5b361936c6f284c4fd1c03ec9227b11ee2d920751abde25", overwrite=True, set_as_default=True) 
service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")
 
circuit = QuantumCircuit(2, 2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure(0,1)
circuit.measure(1,0)
#circuit.draw("mpl") 
#plt.show()

layout = {circuit.qubits[0]: 41, circuit.qubits[1]: 53}  # Developer qubit 0 → Physical qubit 41, Developer qubit 1 → Physical qubit 53
transpiled_circuit = transpile(circuit, backend, initial_layout=layout)
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(transpiled_circuit)
sampler = Sampler(backend)
job = sampler.run([isa_circuit]) # Default 4096 shot

# Son klasik bit counts'ta solda
# Bu kısım biten işlemin sonuçlarını görmek için
#service = QiskitRuntimeService()
#job = service.job('cz3ccqtp6030008c93tg')
#job_result = job.result()
# To get counts for a particular pub result, use 
#
#pub_result = job_result[0].data.c.get_counts()
#print(pub_result)
#
# where <idx> is the index of the pub and <classical register> is the name of the classical register. 
# You can use circuit.cregs to find the name of the classical registers.













