/* ============================================================
   schedule.js — 간격 인출 스케줄러 (reusable).
   Zero dependencies.

   Cepeda, Vul, Rohrer, Wixted & Pashler (2008)의 optimal-gap
   ridgeline을 ln(RI) 위에서 보간해 복습 간격을 뽑고,
   항목들을 교차(interleaving)로 배치해 주 단위 표를 그린다.

   측정된 점 (recall 기준, 논문 본문):
     RI   7일  →  최적 간격  1일
     RI  35일  →            11일
     RI  70일  →            21일
     RI 350일  →            21일

   <div class="widget" data-schedule
        data-days="162"
        data-items="검색/RAG,평가,비용,안전성,파인튜닝,시스템 판단">
     <h3>제목</h3>
     <p class="caption">설명</p>
   </div>
   ============================================================ */

(function () {
  'use strict';

  var RIDGE = [[7, 1], [35, 11], [70, 21], [350, 21]];

  /* ln(RI) 위 선형 보간. 범위를 벗어나면 양 끝으로 고정한다. */
  function optimalGap(ri) {
    if (ri <= RIDGE[0][0]) return RIDGE[0][1];
    var last = RIDGE[RIDGE.length - 1];
    if (ri >= last[0]) return last[1];
    for (var i = 0; i < RIDGE.length - 1; i++) {
      var a = RIDGE[i], b = RIDGE[i + 1];
      if (ri <= b[0]) {
        var t = (Math.log(ri) - Math.log(a[0])) / (Math.log(b[0]) - Math.log(a[0]));
        return a[1] + t * (b[1] - a[1]);
      }
    }
    return last[1];
  }

  function initSchedule(root) {
    var items = (root.getAttribute('data-items') || '').split(',')
      .map(function (s) { return s.trim(); })
      .filter(Boolean);
    var days0 = parseInt(root.getAttribute('data-days'), 10) || 180;

    var ctrl = document.createElement('div');
    ctrl.className = 'control';
    ctrl.innerHTML =
      '<label>목표일까지 남은 날 <span class="val"></span></label>' +
      '<input type="range" min="30" max="270" step="1">';
    root.appendChild(ctrl);

    var readout = document.createElement('div');
    readout.className = 'readout';
    readout.innerHTML =
      '<div class="metric"><span class="k">권장 복습 간격</span><span class="v hl" data-k="gap"></span></div>' +
      '<div class="metric"><span class="k">남은 기간 대비</span><span class="v" data-k="pct"></span></div>' +
      '<div class="metric"><span class="k">항목당 인출 횟수</span><span class="v" data-k="reps"></span></div>';
    root.appendChild(readout);

    var wrap = document.createElement('div');
    wrap.className = 'scroll-x';
    var grid = document.createElement('table');
    grid.className = 'sched';
    wrap.appendChild(grid);
    root.appendChild(wrap);

    var legend = document.createElement('p');
    legend.className = 'sched-legend';
    legend.innerHTML =
      '<span class="key"><i class="first"></i>처음 학습</span>' +
      '<span class="key"><i class="rep"></i>인출 (자료 덮고 꺼내기)</span>';
    root.appendChild(legend);

    var slider = ctrl.querySelector('input');
    var valEl = ctrl.querySelector('.val');
    slider.value = Math.min(270, Math.max(30, days0));

    function render() {
      var days = Number(slider.value);
      var gap = optimalGap(days);
      var gapD = Math.max(1, Math.round(gap));
      var weeks = Math.ceil(days / 7);
      var n = items.length || 1;

      valEl.textContent = days + '일 · 약 ' + weeks + '주';
      readout.querySelector('[data-k="gap"]').textContent = gapD + '일';
      readout.querySelector('[data-k="pct"]').textContent =
        (100 * gapD / days).toFixed(1) + '%';

      var rows = [];
      var maxReps = 0;
      for (var i = 0; i < n; i++) {
        var first = Math.round(i * gapD / n);
        var marks = {};
        var reps = 0;
        for (var d = first, k = 0; d <= days; d += gapD, k++) {
          marks[Math.floor(d / 7)] = (k === 0) ? 'first' : 'rep';
          if (k > 0) reps++;
        }
        maxReps = Math.max(maxReps, reps);
        rows.push({ name: items[i], marks: marks });
      }
      readout.querySelector('[data-k="reps"]').textContent = maxReps + '회';

      var html = '<tr><th>항목</th>';
      for (var w = 0; w < weeks; w++) html += '<th class="wk">' + (w + 1) + '</th>';
      html += '</tr>';
      rows.forEach(function (r) {
        html += '<tr><td class="name">' + r.name + '</td>';
        for (var w = 0; w < weeks; w++) {
          var m = r.marks[w];
          html += '<td class="cell' + (m ? ' ' + m : '') + '"></td>';
        }
        html += '</tr>';
      });
      grid.innerHTML = html;
    }

    slider.addEventListener('input', render);
    render();
  }

  function boot() {
    document.querySelectorAll('[data-schedule]').forEach(initSchedule);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
