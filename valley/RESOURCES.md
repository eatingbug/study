# Index DCF / 매크로 밸류에이션 Resources

## Knowledge

### 1차 자료 — 밸류에이션 이론
- [Damodaran: Historical Implied Equity Risk Premiums (NYU Stern)](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histimpl.html)
  1960~2025년 미국 시장의 **내재 ERP** 연간 시계열. 엑셀 다운로드 가능. 2025년 기준 4.23%. 월가아재 칼럼의 "레짐별 ERP 평균"(61~72년 3.3%, 73~84년 5.2%, ...)은 전부 이 파일에서 나온다. → **레짐 구간을 직접 계산해 보고 싶을 때, ERP 입력값의 근거가 필요할 때.**
- [Damodaran On-line 메인 페이지](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm)
  2008년 9월부터 **매월 초** S&P 500 내재 ERP를 갱신해 첫 페이지에 게시. 2026년 7월 1일 기준 S&P 7,499.36에서 내재 ERP 4.42% (Aa1 디폴트 스프레드 0.22% 차감 시 성숙시장 프리미엄 4.20%). → **숙제 실행 시점의 최신 내재 ERP를 뽑을 때 여기가 1순위.**
- [Damodaran, "The Price of Risk: An Equity Risk Premium Monologue!" (2026-03)](https://aswathdamodaran.blogspot.com/2026/03/the-price-of-risk-equity-risk-premium.html)
  ERP를 왜 과거 데이터로 추정하면 안 되는지, 내재 ERP가 무엇인지 본인이 직접 설명한 글. → **숙제 2번(과거 ERP의 문제점 + 내재 ERP 설명)의 근거로 인용하기 좋음.**
  → 검증된 요약 + verbatim 인용문: `raw/damodaran-2026-03-price-of-risk-요약.md` (2026-08-06). 확인된 수치: 과거방식 범위 5.5~14.5%(2026년 초), 내재 ERP 4.23%, 2008-09-12 4.2%. 주의 — **"내재 ERP의 순환논리"는 이 글에 없는 논점**이다. 원문 논리에서 유도해야 하며 다모다란 인용으로 쓰면 안 된다.
- **과거 ERP 추정치의 표준오차** — 1928~2022년(94년) 10년물 국채 대비 산술평균 **6.64%**, 표준오차 **2.15%p** → 95% 신뢰구간 **2.34% ~ 10.94%**. 표준오차 자체가 연간 수익률의 독립을 가정하므로 과소평가된 값이라는 단서도 함께 확인. 원출처는 다모다란의 ERP 시리즈(`ERP2009.pdf` · `PriceofRisk2023.pdf` · `riskprem.pdf`, 전부 pages.stern.nyu.edu). → **숙제 2번(과거 방식의 문제점)의 가장 강한 한 줄.** L0005 §1의 근거.
  → ⚠️ **2026-08-25 세션에서는 검색 결과 경유로만 확인했다** (egress 정책이 pages.stern.nyu.edu를 차단). 원문 PDF에서 기준 기간·채권 종류·표준오차를 직접 확인해 이 표시를 지울 것.
- **내재 ERP의 계산 절차 (IRR)** — 배당 + 자사주 매입을 현금흐름으로 놓고 그 현재가치를 지수 수준과 같게 만드는 할인율(내부수익률)을 찾은 뒤 무위험수익률을 뺀다. 채권의 만기수익률과 같은 논리. 전제는 **"주식이 총체적으로 올바르게 가격이 매겨져 있다고 가정하면(assuming that stocks are correctly priced in the aggregate)"**. → **순환논리 논증의 출발점. 전제는 인용할 수 있고 결론은 내 논증이다.** L0005 §2의 근거. ⚠️ 위와 같은 경유 확인.
- **다모다란 게시값 갱신** — 2026-08-01 기준 내재 ERP **4.23%**, 기대수익률 **8.97%** (→ 10년물 4.74%). 2026-07-01은 ERP 4.20%(성숙시장 기준) / 기대수익률 8.65% / 10년물 4.45%. 뉴스 경유 확인.
- [Damodaran, "Myth 5.5: The Terminal Value ate my DCF!" (2016-11)](https://aswathdamodaran.blogspot.com/2016/11/myth-55-terminal-value-ate-my-dcf.html)
  종료가치가 전체 가치의 대부분을 차지하는 것이 왜 결함이 아닌지 (주식 수익의 67~85%가 배당이 아닌 가격 상승에서 오므로), 그리고 "TV가 지배하니 근미래 가정은 덜 중요하다"가 왜 **위험한 논리적 비약(dangerous leap of logic)**인지. TV 비중이 고성장 기간의 길이·성장률에 따라 크게 달라진다는 표도 있다. → **숙제 리포트에서 종료가치 가정을 방어할 때, 스터디 라운지에서 "TV가 87%면 못 믿는 것 아니냐"는 반론에 답할 때.** L0002의 1차 자료.
- [Damodaran, "Myth 5.3: Growth is good, more growth is better!" (2016-11)](https://aswathdamodaran.blogspot.com/2016/11/myth-53-growth-is-good-more-growth-is.html)
  성장은 공짜가 아니며 재투자로 값을 치러야 한다(`g = 유보율 × ROE`)는 것, 그리고 **가치를 만드는 것은 성장률 자체가 아니라 초과수익(ROE − 요구수익률)**이라는 것. 검증된 인용: *"Growth is not free and it has to be paid for with reinvestment and in the terminal value equation, this effectively means that you cannot leave cash flows fixed and change the growth rate."* → **숙제에서 10-1번(g)과 10-4번(ROE) 조합을 방어할 때.** L0003의 1차 자료.
- [Damodaran, "Probabilistic Valuation: Scenario Analysis, Decision Trees and Simulations" (Ch.3, PDF)](https://pages.stern.nyu.edu/~adamodar/pdfiles/DSV2/Ch3.pdf)
  시나리오 분석을 언제 쓰고, 몇 개를 만들고, 확률을 어떻게 붙이는지. 앞쪽 시나리오 분석 절만 읽으면 되고 뒤쪽 의사결정나무·몬테카를로는 아직 불필요. 확인된 것: **시나리오는 서너 개까지가 실용 범위**이고, 시나리오들이 "완전한 스펙트럼"을 이룰 때만 가중평균이 기댓값이 된다. → **숙제 3번에서 세 시나리오와 확률 배정을 방어할 때.** L0006의 1차 자료.
  → ⚠️ **2026-08-27 세션에서도 원문 fetch에 실패했다** (egress가 `pages.stern.nyu.edu`·`papers.ssrn.com`을 차단). 검색 결과 경유 확인이며, 같은 내용의 SSRN판은 "Facing Up to Uncertainty: Using Probabilistic Approaches in Valuation"(abstract_id=3237778). **사용자 브라우저에서는 열리므로 레슨에 링크는 걸어 두었다.**
- [Damodaran, Valuation 강의 패킷 1 (Spring 2026, PDF)](https://pages.stern.nyu.edu/~adamodar/pdfiles/eqnotes/valpacket1spr26.pdf)
  DCF의 정석 교재. 할인율, 종료가치, 성장률의 내부 일관성(g = ROE × 유보율)이 전부 여기 있다. → **어떤 공식의 "정통" 근거가 필요할 때.**

### 1차 자료 — 금리 입력값
- [Philadelphia Fed, Survey of Professional Forecasters](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/survey-of-professional-forecasters)
  분기별(2·5·8·11월 중순) 발표. 전문 예측가들의 10년물 국채금리 전망을 향후 몇 개 분기·연간·**향후 10년 평균**까지 낸다. 2026년 1분기 서베이 기준 향후 10년 평균 10년물 = 4.00%. → **근미래(n=1~3) 무위험수익률 입력값의 근거.** 월가아재가 쓰는 바로 그 자료.
- [SPF 데이터 파일: BOND10 (향후 10년 평균 10년물 전망)](https://www.philadelphiafed.org/surveys-and-data/bond10)
  위 서베이의 장기 10년물 전망 시계열 원본 파일.
- [SPF 데이터 파일: TBOND (10년물 단기 분기 전망)](https://www.philadelphiafed.org/surveys-and-data/tbond)
  분기 단위 10년물 전망 시계열.
- FOMC Summary of Economic Projections (SEP) — federalreserve.gov 의 각 FOMC 회의 자료
  점도표와 함께 나오는 **longer-run** 연방기금금리·PCE 전망. `중립 실질금리 = longer-run FFR − longer-run PCE`. 칼럼에서는 3.1% − 2.0% = 1.1%. → **장기 무위험수익률 3분해의 첫 항.**
- FRED: `T10YIE` (10년 기대인플레이션 = 10년물 명목 − 10년물 TIPS)
  시장이 보는 기대 인플레이션. 단 **CPI 기준**이므로 PCE 기준으로 쓰려면 (CPI − PCE) 갭만큼 보정 필요. → **3분해의 두 번째 항.**
- [Kim, Walsh & Wei, "Tips from TIPS: Update and Discussions" (FEDS Notes, 2019-05-21)](https://www.federalreserve.gov/econres/notes/feds-notes/tips-from-tips-update-and-discussions-20190521.html)
  연준 이코노미스트 셋이 브레이크이븐을 분해한 짧은 노트. 검증된 인용(2026-08-22 fetch): *"TIPS IC = expected inflation + inflation risk premium – TIPS liquidity premium."* / *"policymakers and market participants are also cognizant that this spread is an imperfect measure, as it contains other components that can drive a wedge between inflation compensation and market participants' true inflation expectations."* 유동성 프리미엄은 *"believed to have been positive and sizeable in the 1970s and 1980s… but appears to have declined in recent decades to lower or even negative levels."* 주의 — **이 노트는 크기를 정량적으로 제시하지 않는다.** → **3분해의 두 번째 항을 방어할 때, "브레이크이븐을 그대로 기대 인플레로 썼다"는 반론에 답할 때.** L0004의 1차 자료.
- FRED: `THREEFYTP10` (ACM 10년물 기간 프리미엄)
  뉴욕 연은 ACM 모형의 기간 프리미엄 추정치. 칼럼은 시나리오별로 0.5 / 1.2 / 2.0%를 자의적으로 부여했는데, 그 값이 역사적으로 어느 수준인지 대조할 때 유용. → **3분해의 세 번째 항.**

### 데이터 — EPS / 주주환원율
- Yardeni Research (yardeni.com)
  S&P 500 실적 컨센서스와 주주환원율 데이터를 **주 단위**로 공개. 다모다란도 자주 참조. → **1번(EPS 추정)과 2·3번(배당성향·바이백성향)의 근거.**
- S&P Dow Jones Indices, "S&P 500 Earnings and Estimates" 스프레드시트
  지수 산출 주체가 직접 내는 공식 EPS/배당 데이터. 가장 신뢰도 높은 원천.
- Valley AI 가치평가 탭 — Index DCF (valley.town)
  숙제를 실제로 수행하는 도구. 항목별 차트 아이콘을 누르면 과거 25년 평균이 나온다 (배당성향 33.72%, 바이백 47%, 합계 80.72%).

### 강의 (본 과정)
- 월가아재 글로벌 매크로 지식편 6회차 1강 — 자산군 관점에서의 주식
- 월가아재 글로벌 매크로 지식편 6회차 2강 — 주가지수의 DCF  ← **Week 9의 핵심 진도**
- 원문 칼럼: `raw/(월가아재 멘토링) Week 9 - S&P 500의 적정주가를 구해보자!.md`

## Wisdom (Communities)
- **월가아재 스터디 라운지 > 글로벌 매크로 지식편 > 6회차 > 숙제 탭**
  ([링크](https://www.valley.town/study-lounge/assignment?courseId=645b74bed035f958a0cd4053&categoryId=gm.part06))
  Week 9는 숙제 3번을 **전원 공유**하기로 되어 있다. 다른 참가자들이 어떤 가정을 넣어 어떤 숫자를 뽑았는지가 곧 벤치마크. → **내 가정이 이상한지 아닌지 확인하는 가장 값싼 방법.** Week 12 이후 우수작 시상.
- r/SecurityAnalysis (reddit)
  DCF 가정과 밸류에이션 논쟁이 실제로 오가는 곳. 모더레이션 강함. → **내 종료가치 가정을 영어권 기준으로 검증받고 싶을 때.**

> 사용자에게 커뮤니티 참여 의향을 아직 확인하지 않음. 원치 않으면 이 섹션은 정리한다.

> **원문 대조 (2026-08-25).** 사용자가 Week 9 칼럼 원문을 첨부해 L0005의 주장을 전부 대조했다. 확인된 것: ERP 세 값은 `ERP = 총요구수익률 − 무위험수익률` 분해로 레짐에 배정된 도출값이라는 것, EPS 수렴 경로의 시나리오별 산문, ROE 19.45% 검산, 가중평균 7,040. 상세와 남은 불일치는 [NOTES.md](./NOTES.md) → "원문 대조 완료". **원문 자체는 저장소에 넣지 않는다** (`raw/` 정책).

## Gaps
- **`g = ROE × 유보율`의 한계에 대한 1차 자료 미확보.** 평균 ROE ≠ 한계 ROE(신규 투자 수익률), 부채·M&A·마진개선 경로 누락, 장부 자기자본이 투입자본의 나쁜 대리변수라는 점, 자사주 매입이 ROE를 부풀리는 점 — 이 논점들은 **다모다란 Myth 5.3에 없다**(2026-08-07 확인). 숙제에 쓰려면 별도 출처가 필요하다. 다음 후보: Valuation 강의 패킷 1의 성장률 챕터, Damodaran의 ROIC/excess return 관련 글.
- **ERP 레짐별 평균 6개 (3.3 / 5.2 / 3.3 / 3.8 / 5.4 / 4.8%)** — 다모다란이 발표한 값이 아니라 **월가아재가 시계열을 임의 구간으로 잘라 계산한 값**이다. 구간 경계도 그의 판단. 숙제에 근거로 쓰려면 histimpl 엑셀을 받아 직접 검산할 것. **미검산 상태** — L0005는 이 표를 레퍼런스에만 두고, 레슨 본문에서는 각 값이 지수로 얼마인지만 가르친다(구간 평균 자체를 인용하지 않는다). L0005 §5에 "구간을 인용하지 말고 직접 계산하라"를 명시했다.
- **네트워크 제약 (2026-08-25 · 2026-08-27 두 세션 모두)** — 이 환경의 egress 정책이 `pages.stern.nyu.edu` · `aswathdamodaran.blogspot.com` · `aswathdamodaran.substack.com` · `stocktwits.com`을 모두 차단했다. WebSearch는 동작하므로 사실 확인은 가능하지만 **원문 verbatim 인용은 불가**. 다모다란 자료를 새로 검증해야 하는 작업은 egress가 열린 환경에서 할 것.
- ~~**Valley AI Index DCF의 정확한 계산 규약**~~ → **해결 (2026-08-22).** 역검증으로 규약을 확정, ±3.6% 재현. [LR0004](./learning-records/0004-valley-ai-calculation-convention-back-verified.md). 남은 미확인은 **n=4~10 EPS 수렴 경로**뿐이며, 칼럼 산문과 재현 조건이 어긋난다.
- **CPI − PCE 갭의 공식 시계열** — 칼럼은 "현재 서베이상 0.18%, 장기평균 0.30%, 절충 0.26%"라고 하는데 출처 미확인. BEA/BLS 원자료로 직접 계산하는 절차가 필요.
- **민감도 수치 불일치 (신규, 2026-08-25)** — 칼럼은 "무위험수익률 1% 상승 → 적정주가 −700"이라 하는데 내 모델은 현상유지 기준 −1,111이다(−16.0%). 예시용 어림수일 가능성이 높지만 미확인. **L0007 착수 전에 Valley AI 화면에서 10-2번만 1%p 흔들어 실제 변화폭을 기록할 것.** 이게 어긋나면 L0007이 틀린 숫자를 가르친다.
- **S&P 500 장기 ROE 시계열** — 칼럼이 인용한 "1950년대 이후 10~14% → 95년 이후 13~18% → 21~25년 18~21%" 밴드의 원출처 미확인.
