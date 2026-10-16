"""Export browser data from the repository's original comparison Hamiltonian."""
import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

ROOT = Path(__file__).resolve().parents[1]
# Reuse definitions without executing run.py's result-writing top-level loop.
source = (ROOT / 'research/bismuth_heterostructure/run.py').read_text()
namespace = {'__file__': str(ROOT / 'research/bismuth_heterostructure/run.py')}
exec(source.split("names=['Bulk A7 Bi proxy'")[0], namespace)
grid = np.linspace(-2.3, 2.3, 650)
models = []
for kind in range(3):
    values, vectors = eigh(namespace['build'](kind))
    weights = (abs(vectors.reshape(48, 4, -1)) ** 2).sum(axis=1)
    iprs = (weights ** 2).sum(axis=0)
    near = np.argsort(abs(values))[:12]
    dos = np.exp(-.5 * ((grid[:, None] - values[None, :]) / .065) ** 2).sum(axis=1) / (len(values) * .065 * np.sqrt(2 * np.pi))
    models.append({'dos': dos.tolist(), 'states': [
        {'e': float(values[i]), 'ipr': float(iprs[i]), 'weights': weights[:, i].tolist()}
        for i in near]})
payload = {'energy': grid.tolist(), 'models': models, 'seed': 83, 'broadening': .065}
(ROOT / 'app/model-data.js').write_text('window.MODEL_DATA = ' + json.dumps(payload, separators=(',', ':')) + ';\n')
print('Exported 650 DOS samples and 12 states per model.')
