/* ============================================================
   dcf.js — the arithmetic of discounting, shared across lessons.

   Deliberately primitives-only for now. The full two-part Index
   DCF (near-term path + terminal value with 주주환원율 = 1 − g/ROE)
   goes in here once it has been back-checked against the column's
   own results (9,513 / 6,710 / 5,407). Until then, guessing at
   Valley AI's exact convention would teach the wrong thing.
   See NOTES.md → "미결 / 확인 필요".
   ============================================================ */

(function (global) {
  'use strict';

  var DCF = {};

  /* ---------- core discounting ---------- */

  /** 할인계수 discount factor: 1 / (1+r)^t.  r as a decimal (0.10 = 10%). */
  DCF.df = function (r, t) {
    return 1 / Math.pow(1 + r, t);
  };

  /** 현재가치 present value of a single cash flow arriving at year t. */
  DCF.pv = function (cf, r, t) {
    return cf * DCF.df(r, t);
  };

  /** PV of a cash-flow array. cfs[0] arrives at year 1, cfs[1] at year 2, ... */
  DCF.pvSeries = function (cfs, r) {
    return cfs.reduce(function (sum, cf, i) {
      return sum + DCF.pv(cf, r, i + 1);
    }, 0);
  };

  /** Same, but with a different discount rate per year (compounded through). */
  DCF.pvSeriesVarying = function (cfs, rates) {
    var sum = 0, compound = 1;
    for (var i = 0; i < cfs.length; i++) {
      compound *= (1 + (rates[i] !== undefined ? rates[i] : rates[rates.length - 1]));
      sum += cfs[i] / compound;
    }
    return sum;
  };

  /**
   * 고든 성장 모형 / 무한등비급수의 합.
   * A cash flow of cfNext arriving one year from the valuation point and
   * growing at g forever, valued AT that point (not discounted back).
   *   TV = cfNext / (r − g)
   * Returns Infinity when g >= r — the model breaks down there, and that
   * blow-up is itself worth seeing.
   */
  DCF.gordon = function (cfNext, r, g) {
    if (g >= r) return Infinity;
    return cfNext / (r - g);
  };

  /** 할인율 = 무위험수익률 + 리스크 프리미엄. All decimals. */
  DCF.discountRate = function (riskFree, erp) {
    return riskFree + erp;
  };

  /** 주주환원율 = 1 − g / ROE.  (from g = ROE × 유보율) */
  DCF.payoutFromGrowth = function (g, roe) {
    return 1 - g / roe;
  };

  /** g = ROE × 유보율 = ROE × (1 − 주주환원율) */
  DCF.growthFromPayout = function (roe, payout) {
    return roe * (1 - payout);
  };

  /* ---------- formatting ---------- */

  DCF.fmt = function (n, digits) {
    if (!isFinite(n)) return '∞';
    var d = digits === undefined ? 2 : digits;
    return n.toLocaleString('ko-KR', {
      minimumFractionDigits: d,
      maximumFractionDigits: d
    });
  };

  DCF.pct = function (n, digits) {
    var d = digits === undefined ? 2 : digits;
    return (n * 100).toFixed(d) + '%';
  };

  /* ---------- tiny UI helpers (shared by lesson widgets) ---------- */

  /**
   * Wire a range input to a live readout and a redraw callback.
   *   DCF.bindRange('#r', function (val) { ... });
   * Expects markup: <input type="range" id="r"> and an element
   * [data-for="r"] to receive the formatted value.
   */
  DCF.bindRange = function (selector, format, onChange) {
    var el = document.querySelector(selector);
    if (!el) return null;
    var out = document.querySelector('[data-for="' + el.id + '"]');
    function paint() {
      var v = parseFloat(el.value);
      if (out) out.textContent = format(v);
      if (onChange) onChange(v);
    }
    el.addEventListener('input', paint);
    paint();
    return el;
  };

  /** Render a simple bar chart into a container. values: array of numbers. */
  DCF.drawBars = function (container, values, labels, opts) {
    var o = opts || {};
    var max = Math.max.apply(null, values.concat([o.max || 0]));
    container.innerHTML = '';
    values.forEach(function (v, i) {
      var bar = document.createElement('div');
      bar.className = 'bar';
      var track = document.createElement('div');
      track.className = 'track';
      var fill = document.createElement('div');
      fill.className = 'fill' + (o.solid ? ' solid' : '');
      fill.style.height = (max > 0 ? Math.max(1, (v / max) * 100) : 1) + '%';
      var lbl = document.createElement('div');
      lbl.className = 'lbl';
      lbl.textContent = labels && labels[i] !== undefined ? labels[i] : String(i + 1);
      track.appendChild(fill);
      bar.appendChild(track);
      bar.appendChild(lbl);
      container.appendChild(bar);
    });
  };

  global.DCF = DCF;
})(window);
