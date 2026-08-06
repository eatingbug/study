/* ─────────────────────────────────────────────────────────────
   quiz.js — 리트리벌 연습용 퀴즈 위젯 (의존성 없음)
   assets/widgets.css 와 함께 쓴다.

   마크업 규약
   ───────────
   <section class="quiz" data-quiz>
     <div class="widget-head">
       <span class="widget-hint">…</span>
       <span class="score-pill" data-score></span>
     </div>

     <div class="q" data-answer="2">          <!-- 0-based 정답 인덱스 -->
       <p class="q-text">질문</p>
       <ul class="opts">
         <li>선택지 A</li> <li>선택지 B</li> <li>선택지 C</li> <li>선택지 D</li>
       </ul>
       <div class="explain">정답 해설 (정답 선택 전까지 숨겨짐)</div>
     </div>
     …
     <div class="quiz-result" data-result></div>
   </section>

   동작
   ───
   - 선택지 클릭 → 즉시 채점. 정답이면 초록, 오답이면 빨강 + 정답도 함께 표시.
   - 한 문항은 한 번만 답할 수 있다 (재시도 불가 = 리트리벌 강도 유지).
   - 선택지 순서는 로드 시 셔플된다 → 같은 문서를 다시 열어도 위치 암기가 안 된다.
   - 전 문항 완료 시 결과 요약을 노출한다.
   ───────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  function shuffle(nodes) {
    // Fisher–Yates 로 배열을 섞고 그 순서대로 다시 append 한다.
    // (DOM 노드를 직접 swap 하려 하면 균등하지 않게 섞인다.)
    // 정답은 인덱스가 아니라 DOM 노드로 추적하므로 셔플에 안전하다.
    if (!nodes.length) return;
    var parent = nodes[0].parentNode;
    var order = nodes.slice();
    for (var i = order.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = order[i]; order[i] = order[j]; order[j] = t;
    }
    order.forEach(function (n) { parent.appendChild(n); });
  }

  function initQuiz(quiz) {
    var questions = [].slice.call(quiz.querySelectorAll('.q'));
    var scoreEl   = quiz.querySelector('[data-score]');
    var resultEl  = quiz.querySelector('[data-result]');
    var total     = questions.length;
    var answered  = 0;
    var correct   = 0;

    function paintScore() {
      if (scoreEl) scoreEl.textContent = answered + ' / ' + total + '  ·  정답 ' + correct;
    }

    questions.forEach(function (q, qi) {
      var opts    = [].slice.call(q.querySelectorAll('.opts > li'));
      var answer  = opts[parseInt(q.getAttribute('data-answer'), 10)];
      var qText   = q.querySelector('.q-text');

      if (qText && !qText.querySelector('.q-num')) {
        var num = document.createElement('span');
        num.className = 'q-num';
        num.textContent = 'Q' + (qi + 1);
        qText.insertBefore(num, qText.firstChild);
      }

      shuffle(opts);

      opts.forEach(function (opt) {
        opt.setAttribute('role', 'button');
        opt.setAttribute('tabindex', '0');

        function choose() {
          if (q.classList.contains('done')) return;
          q.classList.add('done');
          answered++;

          if (opt === answer) {
            correct++;
            opt.classList.add('correct');
          } else {
            opt.classList.add('wrong');
            answer.classList.add('correct');
          }
          opts.forEach(function (o) { o.removeAttribute('tabindex'); });
          paintScore();

          if (answered === total && resultEl) {
            var pct = Math.round((correct / total) * 100);
            var verdict = correct === total
              ? '전부 맞았다. 이 레슨의 개념은 인출 가능한 상태다 — 이제 실습으로 넘어가자.'
              : (pct >= 60
                ? '대체로 잡혔다. 틀린 문항의 해설만 다시 읽고, 며칠 뒤 이 퀴즈를 다시 풀어라.'
                : '아직 저장 강도가 약하다. 본문을 다시 읽지 말고, 먼저 기억에서 답을 꺼내보려 시도한 뒤 확인해라.');
            resultEl.innerHTML = '<strong>' + correct + ' / ' + total + '</strong> — ' + verdict;
            resultEl.classList.add('show');
          }
        }

        opt.addEventListener('click', choose);
        opt.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choose(); }
        });
      });
    });

    paintScore();
  }

  function boot() {
    [].slice.call(document.querySelectorAll('[data-quiz]')).forEach(initQuiz);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
