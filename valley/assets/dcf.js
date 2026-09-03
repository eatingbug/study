/* ============================================================
   dcf.js — the arithmetic of discounting, shared across lessons.

   The full two-part Index DCF now lives here as DCF.indexDCF, with
   the calculation convention back-checked against the column's own
   three results (9,513 / 6,710 / 5,407) — all three reproduce within
   3.6% under one common EPS glide. See learning-records/0004.
   DCF.solveERP runs the same model backwards — market price in, ERP out.
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

  /**
   * 2단 DCF — 교과서 그대로의 구조. 근미래 n년 + 종료가치.
   *
   * NOTE: 이것은 *예시용 구조 모델*이지 Valley AI의 Index DCF 재현이 아니다.
   * Valley AI의 정확한 계산 규약(연도별 할인율 처리, 주당 기준 등)은 아직
   * 미확인이므로 (NOTES.md → 미결), 칼럼의 9,513 / 6,710 / 5,407 을 이 함수로
   * 재현하려 들지 말 것. 여기서 가르치는 것은 '비중의 구조'다.
   *
   *   cfs  — 1년차부터 n년차까지의 현금흐름 배열
   *   r, g — 소수 (0.091 = 9.1%)
   * 반환: { near, tv, tvPV, total, tvShare }
   */
  DCF.twoPart = function (cfs, r, g) {
    var n = cfs.length;
    var near = DCF.pvSeries(cfs, r);
    var tv = DCF.gordon(cfs[n - 1] * (1 + g), r, g);   // n년차 시점의 값
    var tvPV = tv * DCF.df(r, n);                       // 현재까지 끌고 온 값
    var total = near + tvPV;
    return {
      near: near,
      tv: tv,
      tvPV: tvPV,
      total: total,
      tvShare: total > 0 ? tvPV / total : NaN
    };
  };

  /**
   * 근미래 EPS 경로 만들기 — 앞의 `hold`년은 컨센서스 성장률을 유지하고,
   * 그 뒤로 영구성장률 g까지 선형으로 수렴시킨다.
   * 월가아재가 "n = 4~10에 걸쳐 영구성장률에 수렴시킨다"고 한 그 경로.
   */
  DCF.convergePath = function (cf1, gStart, g, n, hold) {
    var h = hold === undefined ? 3 : hold;
    var cfs = [cf1];
    for (var t = 2; t <= n; t++) {
      var gt;
      if (t <= h) {
        gt = gStart;
      } else if (n <= h) {
        gt = gStart;
      } else {
        // h+1년차부터 한 칸씩 내려온다. 분모를 (n−h+1)로 두어 마지막 해가
        // g에 '거의' 닿게 하고, 마지막 한 칸의 하락은 종료가치 공식이 받는다.
        // (n−h)로 두면 n=4일 때 12% → g 로 한 번에 떨어지는 절벽이 생긴다.
        gt = gStart + (g - gStart) * ((t - h) / (n - h + 1));
      }
      cfs.push(cfs[cfs.length - 1] * (1 + gt));
    }
    return cfs;
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

  /**
   * 지수 DCF 한 판 — 칼럼/Valley AI의 계산 규약을 재현한 것.
   *
   *   opts = {
   *     eps:        [340.39, 397.87, 446.60],  // 컨센서스 구간 (1번 칸)
   *     payoutNear: 0.8072,                    // 근미래 주주환원율 (2·3번)
   *     riskFree:   0.043,                     // 장기 무위험수익률 (10-2번)
   *     erp:        0.048,                     // 위험 프리미엄 (10-3번)
   *     g:          0.0375,                    // 영구성장률 (10-1번)
   *     roe:        0.13,                      // 장기 ROE (10-4번)
   *     n:          10,                        // 근미래 파트의 마지막 해
   *     glideFrom:  0.1225                     // 수렴 시작 성장률 (28년 EPS 성장률)
   *   }
   *
   * 규약: 근미래는 EPS × 주주환원율을 1~n년 할인, 종료가치는
   * (n+1)년차 현금흐름 ÷ (r − g)를 n년 복리로 재할인. 종료가치의
   * 주주환원율은 1 − g/ROE로 도출한다. r은 전 구간 동일.
   *
   * 검증: 칼럼의 세 시나리오를 ±3.6% 안에서 재현한다. 남은 오차는
   * n=4~10 EPS 경로(관측 불가)에서 온다. 절대값보다 '변화폭'을 볼 것.
   */
  DCF.indexDCF = function (opts) {
    var eps        = opts.eps;
    var payoutNear = opts.payoutNear;
    var g          = opts.g;
    var roe        = opts.roe;
    var n          = opts.n === undefined ? 10 : opts.n;
    var r          = DCF.discountRate(opts.riskFree, opts.erp);
    var payoutTV   = DCF.payoutFromGrowth(g, roe);

    // EPS 경로: 컨센서스 구간 뒤로 g까지 선형 수렴
    var path = eps.slice();
    var glide = n - eps.length;
    for (var k = 1; k <= glide; k++) {
      var gt = opts.glideFrom + (g - opts.glideFrom) * (k / glide);
      path.push(path[path.length - 1] * (1 + gt));
    }

    var cfs  = path.map(function (e) { return e * payoutNear; });
    var near = DCF.pvSeries(cfs, r);
    var tv   = DCF.gordon(path[n - 1] * (1 + g) * payoutTV, r, g);
    var tvPV = tv * DCF.df(r, n);
    var total = near + tvPV;

    return {
      r: r, payoutTV: payoutTV, epsPath: path,
      near: near, tv: tv, tvPV: tvPV, total: total,
      tvShare: total > 0 ? tvPV / total : NaN
    };
  };

  /**
   * 내재 ERP 역산 — 모형을 거꾸로 돌린다.
   *
   * 적정가치 자리에 *현재 시장가격*을 놓고, 그 값을 만들어 내는 ERP를 찾는다.
   * indexDCF는 erp에 대해 단조감소이므로 이분법으로 안전하게 수렴한다.
   *
   *   DCF.solveERP({ ...indexDCF의 opts..., }, 7411)  →  0.04472
   *
   * 주의 — 여기서 실제로 시장가격이 결정하는 것은 **r 하나**다. ERP는
   * r에서 당신이 고른 무위험수익률을 뺀 *잔차*일 뿐이므로, opts.riskFree를
   * 바꾸면 반환값이 그만큼 반대로 움직인다(r은 그대로다). 이 성질이
   * L0005의 핵심이다 — learning-records/0005 참조.
   */
  DCF.solveERP = function (opts, targetIndex) {
    var lo = 0.0001, hi = 0.50;   // 50%면 어떤 현실적 지수보다도 낮은 값이 나온다
    var o = {}, k;
    for (k in opts) o[k] = opts[k];

    function valueAt(e) {
      o.erp = e;
      return DCF.indexDCF(o).total;
    }
    // 구간 검사 — 목표가 도달 불가면 NaN을 준다 (조용히 틀린 값을 주지 않는다)
    if (valueAt(lo) < targetIndex || valueAt(hi) > targetIndex) return NaN;

    for (var i = 0; i < 100; i++) {
      var mid = (lo + hi) / 2;
      if (valueAt(mid) > targetIndex) lo = mid; else hi = mid;
    }
    return (lo + hi) / 2;
  };


  /**
   * 일관성 점검 램프를 그린다 — 규칙 목록을 켜고 끄는 컴포넌트.
   *
   *   DCF.renderChecks(el, [
   *     { rule: '방향', level: 'ok',   msg: '두 칸이 같은 세상을 가리킨다' },
   *     { rule: '검산', level: 'warn', msg: '도출 환원율이 <b>58.7%</b>' }
   *   ]);
   *
   * level은 'ok' | 'warn' | 'bad' | ''(중립). msg는 HTML을 허용한다
   * (레슨이 직접 쓰는 문자열만 넣을 것 — 사용자 입력을 넣지 않는다).
   * 스타일은 style.css의 .checks 에 있다.
   */
  DCF.renderChecks = function (container, checks) {
    var el = typeof container === 'string'
      ? document.querySelector(container) : container;
    if (!el) return;
    el.className = 'checks';
    el.innerHTML = checks.map(function (c) {
      return '<li class="' + (c.level || '') + '">' +
             '<span class="lamp"></span>' +
             '<span class="body"><span class="rule">' + c.rule + '</span>' +
             '<span class="msg">' + c.msg + '</span></span></li>';
    }).join('');
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

  /**
   * 가로 누적 막대 — 두 덩어리의 '비중'을 보여 주는 용도.
   *   DCF.drawSplitBar(el, [{ value: 943, label: '근미래', cls: 'near' },
   *                          { value: 1663, label: '종료가치', cls: 'tv' }]);
   * 세그먼트가 좁으면 라벨은 막대 아래 범례로만 나온다.
   */
  DCF.drawSplitBar = function (container, segments) {
    var total = segments.reduce(function (a, s) { return a + (isFinite(s.value) ? s.value : 0); }, 0);
    container.innerHTML = '';

    var bar = document.createElement('div');
    bar.className = 'splitbar';

    var legend = document.createElement('div');
    legend.className = 'splitlegend';

    segments.forEach(function (s) {
      var share = total > 0 ? s.value / total : 0;

      var seg = document.createElement('div');
      seg.className = 'seg ' + (s.cls || '');
      seg.style.width = (share * 100) + '%';
      if (share > 0.14) seg.textContent = (share * 100).toFixed(1) + '%';
      bar.appendChild(seg);

      var key = document.createElement('span');
      key.className = 'key';
      key.innerHTML = '<i class="' + (s.cls || '') + '"></i>' + s.label +
        ' <b>' + (share * 100).toFixed(1) + '%</b>';
      legend.appendChild(key);
    });

    container.appendChild(bar);
    container.appendChild(legend);
  };


  /**
   * 토네이도 — 기준값 대비 변화율을 좌우로 뻗는 가로 막대로 보여 준다.
   * 민감도(L0007·L0008)에서 "어느 칸이 가장 무거운가"를 한눈에 보는 용도.
   *
   *   DCF.drawTornado(el, [{ label: '기간 프리미엄 +1%p', pct: -16.0, note: '5,839' }], { max: 30 });
   *
   * pct는 백분율 숫자(−16.0). max를 주지 않으면 값들의 최대 절대값으로 스케일한다.
   */
  DCF.drawTornado = function (container, rows, opts) {
    var o = opts || {};
    var max = o.max || Math.max.apply(null, rows.map(function (r) {
      return Math.abs(isFinite(r.pct) ? r.pct : 0);
    }).concat([1]));

    container.innerHTML = '';
    container.className = 'tornado';

    rows.forEach(function (r) {
      var pct = isFinite(r.pct) ? r.pct : 0;
      var share = Math.min(1, Math.abs(pct) / max);

      var row = document.createElement('div');
      row.className = 'trow' + (r.dim ? ' dim' : '');

      var name = document.createElement('div');
      name.className = 'tname';
      name.innerHTML = r.label;

      var track = document.createElement('div');
      track.className = 'ttrack';

      var bar = document.createElement('div');
      bar.className = 'tbar ' + (pct < 0 ? 'neg' : 'pos');
      bar.style.width = (share * 50) + '%';
      track.appendChild(bar);

      var val = document.createElement('div');
      val.className = 'tval';
      val.textContent = (pct > 0 ? '+' : '') + pct.toFixed(1) + '%' +
        (r.note ? '  (' + r.note + ')' : '');

      row.appendChild(name);
      row.appendChild(track);
      row.appendChild(val);
      container.appendChild(row);
    });
  };

  global.DCF = DCF;
})(window);
