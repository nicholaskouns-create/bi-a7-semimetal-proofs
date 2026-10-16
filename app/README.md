# Bismuth playground

An accessible, responsive, browser-only educational visualizer. Open `index.html`
directly, or serve this directory with `python -m http.server 8000`.
No build step or API credentials are required.

Switch materials, tune energy, select any of twelve near-Fermi eigenstates per
model, pause animation, or reset. Chart points also support Tab and Enter/Space.
Reduced-motion preferences pause the animation initially.

`model-data.js` is generated from the repository's original 48-site comparison
Hamiltonian by `python app/export_model.py` (NumPy and SciPy required). It contains
650 broadened DOS samples and twelve near-Fermi eigenstates per model, including
their IPR and site weights. The exported DOS follows the original normalization
per Hamiltonian basis state. The atomic animation remains a conceptual metaphor.
These models are not calibrated experimental spectra and do not demonstrate
superconductivity in a physical specimen.

Eigenvectors in degenerate subspaces can depend on the numerical library.
The bulk near-Fermi IPR average may therefore differ slightly from the archived
run; the UI uses the exported eigenvectors and their directly computed IPR.
