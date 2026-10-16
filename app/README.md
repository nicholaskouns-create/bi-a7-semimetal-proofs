# Bismuth playground

An accessible, responsive, browser-only educational visualizer. Open `index.html`
directly, or serve this directory with `python -m http.server 8000`.
No build step or API credentials are required.

Switch materials, tune energy, select any of twelve near-Fermi eigenstates per
model, pause animation, or reset. Chart points also support Tab and Enter/Space.
Reduced-motion preferences pause the animation initially.

## Hosting

The GitHub Pages workflow publishes only the four public browser assets on pushes
to `main` that change the app. In repository Settings → Pages, choose **GitHub
Actions** as the source once. Then run **Deploy Bismuth playground** from Actions
(or push an app change). Expected URL after a successful deployment:
https://nicholaskouns-create.github.io/bi-a7-semimetal-proofs/

The connected integration cannot enable Pages itself: GitHub returns HTTP 403
for that repository-settings operation. No extra token or repository secret is
needed after the owner enables the GitHub Actions source.

## Validation

Run `node --test app/tests/app.test.cjs`. Tests cover exported state normalization
and IPR, material controls, slider/state synchronization, keyboard selection,
pause/reset, reduced motion, and energy-domain bounds. They use a small DOM
harness, not a rendered browser, so visual layout still needs browser review.

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
