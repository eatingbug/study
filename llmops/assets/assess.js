/* ─────────────────────────────────────────────────────────────
   assess.js — 영역별 자기진단 스코어러 (의존성 없음)
   assets/widgets.css 와 함께 쓴다.

   목적: "내 시스템이 지금 어디가 비어 있는가"를 체크박스로 드러내고,
         가장 약한 영역을 다음 학습 순서로 되돌려준다 (ZPD 계산 보조).

   마크업 규약
   ───────────
   <section class="assess" data-assess data-key="llmops-maturity-v1">
     <div class="widget-head">
       <span class="widget-hint">…</span>
       <span class="score-pill" data-score></span>
     </div>

     <div class="area" data-area="평가(Eval)" data-next="오류분석으로 실패 유형 분류하기">
       <div class="area-head">
         <div class="area-name">평가(Eval) 체계<small>부제</small></div>
         <span class="area-score" data-area-score></span>
       </div>
       <ul class="checks">
         <li><label><input type="checkbox"><span>체크 문항</span></label></li>
       </ul>
       <div class="bar"><i></i></div>
     </div>
     …
     <div class="assess-result" data-result></div>
   </section>

   동작
   ───
   - 체크할 때마다 영역별 점수·진행 바·총점을 즉시 갱신한다 (타이트한 피드백 루프).
   - data-key 가 있으면 localStorage 에 저장 → 다시 열어도 상태가 남는다.
   - 점수가 낮은 영역 3개를 "다음에 다룰 것"으로 정렬해 제시한다.
     동점이면 문서에 적힌 순서를 유지한다 (안정 정렬).
   ───────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  function initAssess(root) {
    var areas    = [].slice.call(root.querySelectorAll('.area'));
    var scoreEl  = root.querySelector('[data-score]');
    var resultEl = root.querySelector('[data-result]');
    var key      = root.getAttribute('data-key');

    var saved = {};
    if (key) {
      try { saved = JSON.parse(localStorage.getItem(key) || '{}') || {}; }
      catch (e) { saved = {}; }
    }

    var models = areas.map(function (area, ai) {
      var boxes = [].slice.call(area.querySelectorAll('.checks input[type=checkbox]'));
      boxes.forEach(function (box, bi) {
        box.checked = !!(saved[ai] && saved[ai][bi]);
        box.addEventListener('change', update);
      });
      return {
        index: ai,
        el: area,
        boxes: boxes,
        name: area.getAttribute('data-area') || ('영역 ' + (ai + 1)),
        next: area.getAttribute('data-next') || '',
        // data-defer: 미션에서 우선순위를 내린 영역.
        // 여전히 체크는 되지만 총점과 "다음에 다룰 것" 순위에서 제외된다.
        defer: area.hasAttribute('data-defer'),
        scoreEl: area.querySelector('[data-area-score]'),
        barEl: area.querySelector('.bar > i')
      };
    });

    function persist() {
      if (!key) return;
      var state = {};
      models.forEach(function (m) {
        state[m.index] = m.boxes.map(function (b) { return b.checked; });
      });
      try { localStorage.setItem(key, JSON.stringify(state)); } catch (e) { /* 무시 */ }
    }

    function update() {
      var hit = 0, all = 0;

      models.forEach(function (m) {
        var n = m.boxes.filter(function (b) { return b.checked; }).length;
        m.hits = n;
        m.ratio = m.boxes.length ? n / m.boxes.length : 0;
        if (!m.defer) { hit += n; all += m.boxes.length; }

        if (m.scoreEl) m.scoreEl.textContent = n + ' / ' + m.boxes.length;
        if (m.barEl) m.barEl.style.width = (m.ratio * 100).toFixed(0) + '%';
      });

      if (scoreEl) {
        scoreEl.textContent = hit + ' / ' + all +
          '  ·  성숙도 ' + (all ? Math.round((hit / all) * 100) : 0) + '%';
      }

      if (resultEl) renderResult(models, hit, all, resultEl);
      persist();
    }

    update();
  }

  function renderResult(models, hit, all, resultEl) {
    var ranked = models.filter(function (m) { return !m.defer; });
    var weak = ranked.slice().sort(function (a, b) {
      return a.ratio - b.ratio || a.index - b.index;   // 동점 시 문서 순서 유지
    }).filter(function (m) { return m.ratio < 1; }).slice(0, 3);

    var deferred = models.filter(function (m) { return m.defer; });
    var html = '';

    if (all && hit === all) {
      html += '<p class="verdict">우선순위 영역이 모두 채워져 있다.</p>' +
              '<p class="empty">체크리스트가 당신보다 뒤처졌다는 뜻이다. ' +
              '기준을 올려라 — 각 영역에서 "숫자로 증명할 수 있는가"를 다시 물어보고, ' +
              '선생(에이전트)에게 더 엄격한 진단 문항을 요청해라.</p>';
    } else if (hit === 0) {
      html += '<p class="verdict">아직 체크한 항목이 없다.</p>' +
              '<p class="empty">지금 운영 중인 서비스를 떠올리면서 정직하게 체크해라. ' +
              '"있다"의 기준은 <em>문서나 코드로 존재하고 다른 사람이 찾을 수 있다</em>는 것이다. ' +
              '머릿속에만 있으면 없는 것이다.</p>';
    } else {
      html += '<p class="verdict">가장 비어 있는 영역 — 이 순서로 다루면 된다:</p><ol>';
      weak.forEach(function (m) {
        html += '<li><strong>' + m.name + '</strong> (' + m.hits + '/' + m.boxes.length + ')' +
                (m.next ? ' → ' + m.next : '') + '</li>';
      });
      html += '</ol>';
    }

    if (deferred.length) {
      html += '<p class="deferred-note">순위 계산에서 제외됨(미션에서 우선순위 하향): ' +
              deferred.map(function (m) {
                return m.name + ' ' + m.hits + '/' + m.boxes.length;
              }).join(' · ') + '</p>';
    }

    resultEl.innerHTML = html;
  }

  function boot() {
    [].slice.call(document.querySelectorAll('[data-assess]')).forEach(initAssess);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
