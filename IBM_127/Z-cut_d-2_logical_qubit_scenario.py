from qiskit import QuantumCircuit
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

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(circuit)
sampler = Sampler(backend)
job = sampler.run([isa_circuit])
result = job.result()
print(f" > Counts: {result[0].data.meas.get_counts()}")
# alttaki klasik bit counts'ta solda













