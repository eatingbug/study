/* ============================================================
   quiz.js — reusable retrieval-practice widgets.
   Zero dependencies. Declarative: write markup, this wires it.

   ---- Multiple choice -------------------------------------
   <div class="quiz" data-quiz>
     <h3>제목</h3>
     <div class="q" data-answer="2">
       <p class="stem">문제</p>
       <div class="opts">
         <button class="opt">보기1</button>
         <button class="opt">보기2</button>
         <button class="opt">보기3</button>
       </div>
       <div class="why">정답 해설</div>
     </div>
     <div class="score"></div>
   </div>

   data-answer is 0-indexed. Keep every 보기 the same character
   count (spaces included) — length differences leak the answer.

   ---- Numeric drill ---------------------------------------
   <div class="drill" data-drill>
     <h3>제목</h3>
     <div class="row" data-answer="90.91" data-tol="0.05">
       <span class="ask">질문</span>
       <input type="text" inputmode="decimal">
       <span class="unit">만원</span>
       <span class="mark"></span>
       <div class="hint">풀이</div>
     </div>
     <div class="actions"><button class="ghost" data-reveal>정답 보기</button></div>
   </div>

   Answers are checked live as you type, within data-tol
   (absolute tolerance, default 0.01).
   ============================================================ */

(function () {
  'use strict';

  /* ---------------- multiple choice ---------------- */

  function initQuiz(root) {
    var questions = Array.prototype.slice.call(root.querySelectorAll('.q'));
    var scoreEl = root.querySelector('.score');
    var answered = 0;
    var correct = 0;

    function paintScore() {
      if (!scoreEl) return;
      if (answered === 0) {
        scoreEl.textContent = questions.length + '문항 — 답을 골라 보세요. 틀려도 됩니다, 틀린 뒤에 남는 게 더 오래갑니다.';
      } else {
        scoreEl.textContent = answered + ' / ' + questions.length + ' 응답 · ' +
          correct + '문항 정답';
        if (answered === questions.length) {
          scoreEl.textContent += correct === questions.length
            ? ' — 전부 맞혔습니다.'
            : ' — 틀린 문항의 해설을 한 번 더 읽어 보세요.';
        }
      }
    }

    questions.forEach(function (q) {
      var answer = parseInt(q.getAttribute('data-answer'), 10);
      var opts = Array.prototype.slice.call(q.querySelectorAll('button.opt'));
      var why = q.querySelector('.why');
      var done = false;

      opts.forEach(function (btn, i) {
        btn.addEventListener('click', function () {
          if (done) return;
          done = true;
          answered++;
          if (i === answer) correct++;

          opts.forEach(function (b, j) {
            b.disabled = true;
            if (j === answer) b.classList.add('correct');
            else if (j === i) b.classList.add('wrong');
          });
          if (why) why.classList.add('show');
          paintScore();
        });
      });
    });

    paintScore();
  }

  /* ---------------- numeric drill ---------------- */

  function parseNum(s) {
    if (typeof s !== 'string') return NaN;
    var cleaned = s.replace(/[,\s%원]/g, '');
    if (cleaned === '' || cleaned === '-' || cleaned === '.') return NaN;
    return Number(cleaned);
  }

  function initDrill(root) {
    var rows = Array.prototype.slice.call(root.querySelectorAll('.row[data-answer]'));

    rows.forEach(function (row) {
      var answer = Number(row.getAttribute('data-answer'));
      var tol = row.hasAttribute('data-tol') ? Number(row.getAttribute('data-tol')) : 0.01;
      var input = row.querySelector('input[type="text"]');
      var mark = row.querySelector('.mark');
      var hint = row.querySelector('.hint');
      if (!input) return;

      input.setAttribute('inputmode', 'decimal');
      input.setAttribute('autocomplete', 'off');

      input.addEventListener('input', function () {
        var v = parseNum(input.value);
        input.classList.remove('ok', 'no');
        if (mark) mark.textContent = '';
        if (hint) hint.classList.remove('show');

        if (isNaN(v)) return;

        if (Math.abs(v - answer) <= tol) {
          input.classList.add('ok');
          if (mark) mark.textContent = '✓';
          if (hint) hint.classList.add('show');
        } else if (input.value.trim().length >= String(Math.trunc(Math.abs(answer))).length) {
          // only flag as wrong once enough digits are typed
          input.classList.add('no');
          if (mark) mark.textContent = '·';
        }
      });
    });

    var reveal = root.querySelector('[data-reveal]');
    if (reveal) {
      reveal.addEventListener('click', function () {
        rows.forEach(function (row) {
          var input = row.querySelector('input[type="text"]');
          var hint = row.querySelector('.hint');
          var mark = row.querySelector('.mark');
          if (input && !input.classList.contains('ok')) {
            input.value = row.getAttribute('data-answer');
            input.classList.remove('no');
            input.classList.add('ok');
            if (mark) mark.textContent = '✓';
          }
          if (hint) hint.classList.add('show');
        });
        reveal.disabled = true;
        reveal.textContent = '정답 표시됨';
      });
    }
  }

  /* ---------------- boot ---------------- */

  function boot() {
    document.querySelectorAll('[data-quiz]').forEach(initQuiz);
    document.querySelectorAll('[data-drill]').forEach(initDrill);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
