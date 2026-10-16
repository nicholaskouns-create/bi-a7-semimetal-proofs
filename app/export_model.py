"""Export browser data from the repository's original comparison Hamiltonian."""
import ast
import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

ROOT = Path(__file__).resolve().parents[1]
# Reuse imports and function definitions without running the output-writing loop.
source = (ROOT / 'research/bismuth_heterostructure/run.py').read_text()
namespace = {'__file__': str(ROOT / 'research/bismuth_heterostructure/run.py')}
module = ast.parse(source)
cutoff = next(i for i, node in enumerate(module.body)
              if isinstance(node, ast.Assign)
              and any(isinstance(target, ast.Name) and target.id == 'names'
                      for target in node.targets))
definitions = ast.Module(body=module.body[:cutoff], type_ignores=[])
exec(compile(definitions, 'bismuth_heterostructure/run.py', 'exec'), namespace)
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
