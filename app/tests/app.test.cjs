const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');

// A small DOM harness checks real handlers without external test dependencies.
function playground(reducedMotion = false) {
  class Element {
    constructor(dataset = {}) {
      this.dataset = dataset;
      this.style = { setProperty() {} };
      this.attributes = {};
      this.classList = { toggle() {} };
      this.textContent = '';
      this.value = 0;
      this.clientWidth = 1100;
      this.clientHeight = 400;
    }
    setAttribute(k, v) { this.attributes[k] = String(v); }
    set innerHTML(value) {
      this.html = value;
      this.points = [...value.matchAll(/data-m="(\d+)" data-i="(\d+)"/g)]
        .map(m => new Element({ m: m[1], i: m[2] }));
    }
    get innerHTML() { return this.html; }
    querySelectorAll() { return this.points || []; }
    querySelector(selector) {
      const m = selector.match(/data-m="(\d+)".*data-i="(\d+)"/);
      return this.points.find(p => p.dataset.m === m[1] && p.dataset.i === m[2]);
    }
    focus() { this.focused = true; }
  }
  const elements = new Map();
  const get = selector => {
    if (!elements.has(selector)) elements.set(selector, new Element());
    return elements.get(selector);
  };
  const materials = [0, 1, 2].map(m => new Element({ material: String(m) }));
  const context2d = new Proxy({}, { get: (_, prop) => prop === 'createRadialGradient'
    ? () => ({ addColorStop() {} }) : () => {} });
  get('#lattice').getContext = () => context2d;
  const context = vm.createContext({
    window: { addEventListener() {} }, document: {
      querySelector: get, querySelectorAll: () => materials,
      documentElement: new Element(), hidden: false,
    }, matchMedia: () => ({ matches: reducedMotion }),
    requestAnimationFrame() {}, devicePixelRatio: 1,
  });
  vm.runInContext(readFileSync(path.join(root, 'model-data.js'), 'utf8'), context);
  vm.runInContext(readFileSync(path.join(root, 'app.js'), 'utf8'), context);
  return { get, materials, context, data: context.window.MODEL_DATA };
}

test('model exports normalized states with internally consistent IPR', () => {
  const { data } = playground();
  for (const model of data.models) {
    assert.equal(model.dos.length, data.energy.length);
    assert.equal(model.states.length, 12);
    for (const state of model.states) {
      assert.ok(Math.abs(state.weights.reduce((a, b) => a + b, 0) - 1) < 1e-10);
      assert.ok(Math.abs(state.weights.reduce((a, b) => a + b * b, 0) - state.ipr) < 1e-10);
      assert.ok(state.e >= -.6 && state.e <= .6);
      assert.ok(state.ipr > 0 && state.ipr < .5);
    }
  }
});

test('all material controls update content and pressed states', () => {
  const { get, materials } = playground();
  materials[2].onclick();
  assert.equal(get('#scene-title').textContent, 'An irregular neighborhood');
  assert.equal(materials[2].attributes['aria-pressed'], 'true');
  assert.equal(materials[0].attributes['aria-pressed'], 'false');
});

test('energy slider updates DOS and clears a previously selected state', () => {
  const { get } = playground();
  get('#ipr').points[25].onclick();
  assert.notEqual(get('#state-value').textContent, '↗');
  get('#energy').oninput({ target: { value: '1.2' } });
  assert.match(get('#energy-value').innerHTML, /1.20/);
  assert.equal(get('#state-value').textContent, '↗');
  assert.ok(Number(get('#dos-value').textContent) > 0);
});

test('keyboard activation selects exact state and returns focus', () => {
  const { get, data } = playground();
  let prevented = false;
  get('#ipr').points[26].onkeydown({ key: 'Enter', preventDefault() { prevented = true; } });
  assert.ok(prevented);
  assert.equal(get('#state-value').textContent, data.models[2].states[2].ipr.toFixed(3));
  assert.equal(Number(get('#energy').value), data.models[2].states[2].e);
  assert.ok(get('#ipr').points[26].focused);
});

test('pause and reset respect reduced-motion preferences', () => {
  const { get, materials } = playground(true);
  assert.match(get('#pause').textContent, /Resume/);
  get('#pause').onclick();
  assert.equal(get('#pause').attributes['aria-pressed'], 'false');
  materials[2].onclick();
  get('#reset').onclick();
  assert.equal(get('#scene-title').textContent, 'A smooth neighborhood');
  assert.equal(Number(get('#energy').value), 0);
  assert.match(get('#pause').textContent, /Resume/);
});

test('energy control bounds agree with exported domain; charts stay finite', () => {
  const { get, context, data } = playground();
  const html = readFileSync(path.join(root, 'index.html'), 'utf8');
  assert.ok(html.includes(`min="${data.energy[0]}" max="${data.energy.at(-1)}"`));
  for (const e of [data.energy[0], 0, data.energy.at(-1)]) {
    get('#energy').oninput({ target: { value: String(e) } });
    assert.ok(!/NaN|Infinity/.test(get('#dos').innerHTML));
  }
  get('#energy').oninput({ target: { value: '0' } });
  assert.ok(Number(get('#dos-value').textContent) > 0, 'small Fermi DOS must not round to zero');
  assert.equal(vm.runInContext('ex(ENERGY_MIN)', context), 42);
  assert.equal(vm.runInContext('ex(ENERGY_MAX)', context), 483);
});
