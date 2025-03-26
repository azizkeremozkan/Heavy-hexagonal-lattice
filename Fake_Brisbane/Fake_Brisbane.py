from qiskit_ibm_runtime.fake_provider import FakeBrisbane
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit.transpiler import Layout, CouplingMap
from qiskit import transpile, QuantumCircuit
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

no_of_qubits = 7  # 0:D1, 1:F1, 2:D2, 3:S1, 4:D3, 5:F2, 6:D4
no_of_classical_bits = 4  # 3:S1'in 1. ölçümü, 2:S1'in 2. ölçümü, 1:F1 (önemli değil), 0:F2 (önemli değil)

def Z_round_of_S1(cycle_no):
    circuit.reset(1)
    circuit.reset(5)
    circuit.cx(0, 1)
    circuit.cx(6, 5)
    circuit.cx(1, 2)
    circuit.reset(3)
    circuit.cx(5, 4)
    circuit.cx(0, 1)
    circuit.cx(2, 3)
    circuit.cx(6, 5)
    circuit.measure(1, 1)
    circuit.reset(1)
    circuit.cx(4, 3)
    circuit.measure(5, 0)
    circuit.reset(5)
    circuit.cx(0, 1)
    circuit.measure(3, (no_of_classical_bits - cycle_no))
    circuit.cx(6, 5)
    circuit.cx(1, 2)
    circuit.cx(5, 4)
    circuit.cx(0, 1)
    circuit.cx(6, 5)
    circuit.measure(1, 1)
    circuit.reset(1)
    circuit.measure(5, 0)
    circuit.reset(5)

def Apply_logical_X():
    circuit.x(6)

# Build the quantum circuit
circuit = QuantumCircuit(no_of_qubits, no_of_classical_bits)
# Başlangıç durumu |-+++>
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
Z_round_of_S1(1)
circuit.barrier()
Apply_logical_X()
circuit.barrier()
Z_round_of_S1(2)
circuit.barrier()

# Load FakeBrisbane and its noise model
fake_backend = FakeBrisbane()
noise_model = NoiseModel.from_backend(fake_backend)

# Define the layout: logical qubits → physical qubits
layout = Layout({
    circuit.qubits[0]: 39,
    circuit.qubits[1]: 40,
    circuit.qubits[2]: 41,
    circuit.qubits[3]: 53,
    circuit.qubits[4]: 60,
    circuit.qubits[5]: 59,
    circuit.qubits[6]: 58
})

# Extract only relevant coupling map edges
cmap = fake_backend.configuration().coupling_map
subset = [39, 40, 41, 53, 60, 59, 58]
reduced_cmap = [pair for pair in cmap if pair[0] in subset and pair[1] in subset]
coupling_map = CouplingMap(reduced_cmap)

# Build simulator with restricted coupling map
simulator = AerSimulator(noise_model=noise_model, coupling_map=coupling_map, basis_gates=noise_model.basis_gates)

# Transpile for the simulator using your layout
transpiled_qc = transpile(
    circuit,
    backend=fake_backend,
    initial_layout=layout,
    routing_method='none',
    optimization_level=0
)

# Simulate
job = simulator.run(transpiled_qc, noise_model=noise_model, shots=4096)
result = job.result()
counts = result.get_counts()

# Visualize
plot_histogram(counts)
plt.title("X applied to Fourth Data Qubit (Qubit 3) on FakeBrisbane with layout")
plt.show()

# Draw circuit
circuit.draw("mpl")
plt.show()

