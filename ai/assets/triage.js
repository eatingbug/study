/* ============================================================
   triage.js — 2축 분류 연습 위젯 (reusable).
   Zero dependencies. 선언적: 마크업을 쓰면 이 파일이 배선한다.

   각 항목에 대해 사용자가 두 개의 예/아니오 판단을 내리면,
   그 판단이 함의하는 사분면을 즉시 보여 주고
   레퍼런스 분류와 비교해 피드백을 준다.

   <div class="triage" data-triage
        data-x-label="검증 가능성" data-y-label="실시간 인출">
     <h3>제목</h3>
     <p class="caption">설명</p>

     <div class="item" data-x="1" data-y="0"
          data-why="레퍼런스 분류의 근거 한두 문장.">
       <p class="task">분류할 일</p>
     </div>
     ...
     <div class="tally"></div>
   </div>

   data-x = 1 이면 "검증 가능", data-y = 1 이면 "실시간 인출 필요".
   축 질문과 사분면 이름은 아래 AXES / QUADRANTS 에서 바꾼다.
   ============================================================ */

(function () {
  'use strict';

  var AXES = {
    x: { q: '이게 틀렸을 때, 내가 알아챌 수 있는가?', yes: '알아챈다', no: '못 알아챈다' },
    y: { q: '면접·설계 회의에서 찾아볼 틈 없이 꺼내야 하는가?', yes: '즉시 꺼낸다', no: '찾아봐도 된다' }
  };

  /* key = x + '' + y */
  var QUADRANTS = {
    '10': { name: '위임',        cls: 'ok',
            gist: '검증할 수 있고 실시간으로 꺼낼 일도 없다. 맡기고, 결과만 확인한다.' },
    '11': { name: '위임 + 인출 드릴', cls: 'warn',
            gist: '맡겨도 되지만 방에서는 맨손으로 꺼내야 한다. AI에게 시키되 따로 인출 연습을 건다.' },
    '00': { name: '검증력 먼저', cls: 'warn',
            gist: '틀려도 모르는 것을 맡기는 건 위임이 아니라 항복이다. 검증할 수 있을 만큼 먼저 익힌다.' },
    '01': { name: '체화',        cls: 'bad',
            gist: '못 알아채는데 즉시 꺼내야 한다. 위임 불가 구간 — 여기가 실력이 되는 자리다.' }
  };

  function initTriage(root) {
    var items = Array.prototype.slice.call(root.querySelectorAll('.item'));
    var tally = root.querySelector('.tally');
    var done = 0, matched = 0;

    function paintTally() {
      if (!tally) return;
      if (done === 0) {
        tally.textContent = items.length + '개 항목 — 두 질문에 답하면 사분면이 정해집니다. ' +
          '레퍼런스와 달라도 됩니다. 어긋난 자리가 이 레슨에서 가장 값어치 있는 지점입니다.';
      } else {
        tally.textContent = done + ' / ' + items.length + ' 분류 · 레퍼런스와 일치 ' + matched + '개';
        if (done === items.length) {
          tally.textContent += (matched === items.length)
            ? ' — 기준이 잡혔습니다.'
            : ' — 어긋난 항목의 근거를 다시 읽어 보세요. 거기가 당신의 경계선이 레퍼런스와 다른 곳입니다.';
        }
      }
    }

    items.forEach(function (item) {
      var refX = item.getAttribute('data-x');
      var refY = item.getAttribute('data-y');
      var why = item.getAttribute('data-why') || '';
      var picked = { x: null, y: null };
      var settled = false;

      var axes = document.createElement('div');
      axes.className = 'axes';

      ['x', 'y'].forEach(function (k) {
        var row = document.createElement('div');
        row.className = 'axis';

        var label = document.createElement('span');
        label.className = 'alabel';
        label.textContent = AXES[k].q;
        row.appendChild(label);

        var btns = document.createElement('span');
        btns.className = 'abtns';
        [['1', AXES[k].yes], ['0', AXES[k].no]].forEach(function (pair) {
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'opt';
          b.textContent = pair[1];
          b.addEventListener('click', function () {
            if (settled) return;
            picked[k] = pair[0];
            Array.prototype.forEach.call(btns.children, function (o) {
              o.classList.remove('picked');
            });
            b.classList.add('picked');
            settle();
          });
          btns.appendChild(b);
        });
        row.appendChild(btns);
        axes.appendChild(row);
      });

      var box = document.createElement('div');
      box.className = 'verdict-box';

      item.appendChild(axes);
      item.appendChild(box);

      function settle() {
        if (picked.x === null || picked.y === null) return;
        settled = true;
        done++;

        var q = QUADRANTS[picked.x + picked.y];
        var agrees = (picked.x === refX && picked.y === refY);
        if (agrees) matched++;

        var v = document.createElement('div');
        v.className = 'verdict ' + (agrees ? q.cls : 'bad');
        v.innerHTML = '<b>' + q.name + '</b> — ' + q.gist;
        box.appendChild(v);

        if (!agrees) {
          var ref = QUADRANTS[refX + refY];
          var d = document.createElement('p');
          d.className = 'refnote';
          d.innerHTML = '레퍼런스 분류는 <b>' + ref.name + '</b>입니다. ' + why;
          box.appendChild(d);
        } else if (why) {
          var w = document.createElement('p');
          w.className = 'refnote agree';
          w.innerHTML = why;
          box.appendChild(w);
        }

        item.classList.add('settled');
        Array.prototype.forEach.call(item.querySelectorAll('.abtns button'), function (b) {
          b.disabled = true;
        });
        paintTally();
      }
    });

    paintTally();
  }

  function boot() {
    document.querySelectorAll('[data-triage]').forEach(initTriage);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
