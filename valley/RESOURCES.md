# Index DCF / 매크로 밸류에이션 Resources

## Knowledge

### 1차 자료 — 밸류에이션 이론
- [Damodaran: Historical Implied Equity Risk Premiums (NYU Stern)](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histimpl.html)
  1960~2025년 미국 시장의 **내재 ERP** 연간 시계열. 엑셀 다운로드 가능. 2025년 기준 4.23%. 월가아재 칼럼의 "레짐별 ERP 평균"(61~72년 3.3%, 73~84년 5.2%, ...)은 전부 이 파일에서 나온다. → **레짐 구간을 직접 계산해 보고 싶을 때, ERP 입력값의 근거가 필요할 때.**
- [Damodaran On-line 메인 페이지](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm)
  2008년 9월부터 **매월 초** S&P 500 내재 ERP를 갱신해 첫 페이지에 게시. 2026년 7월 1일 기준 S&P 7,499.36에서 내재 ERP 4.42% (Aa1 디폴트 스프레드 0.22% 차감 시 성숙시장 프리미엄 4.20%). → **숙제 실행 시점의 최신 내재 ERP를 뽑을 때 여기가 1순위.**
- [Damodaran, "The Price of Risk: An Equity Risk Premium Monologue!" (2026-03)](https://aswathdamodaran.blogspot.com/2026/03/the-price-of-risk-equity-risk-premium.html)
  ERP를 왜 과거 데이터로 추정하면 안 되는지, 내재 ERP가 무엇인지 본인이 직접 설명한 글. → **숙제 2번(과거 ERP의 문제점 + 내재 ERP 설명)의 근거로 인용하기 좋음.**
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

## Gaps
- **ERP 레짐별 평균 6개 (3.3 / 5.2 / 3.3 / 3.8 / 5.4 / 4.8%)** — 다모다란이 발표한 값이 아니라 **월가아재가 시계열을 임의 구간으로 잘라 계산한 값**이다. 구간 경계도 그의 판단. 숙제에 근거로 쓰려면 histimpl 엑셀을 받아 직접 검산할 것. 미검산 상태.
- **Valley AI Index DCF의 정확한 계산 규약** — 연도별 할인율을 쓰는지, 종료가치를 n년으로 할인하는지, 주당(per-share) 기준을 어떻게 처리하는지 문서화된 자료를 못 찾음. 칼럼의 결과값(9,513 / 6,710 / 5,407)으로 역검증 필요.
- **CPI − PCE 갭의 공식 시계열** — 칼럼은 "현재 서베이상 0.18%, 장기평균 0.30%, 절충 0.26%"라고 하는데 출처 미확인. BEA/BLS 원자료로 직접 계산하는 절차가 필요.
- **S&P 500 장기 ROE 시계열** — 칼럼이 인용한 "1950년대 이후 10~14% → 95년 이후 13~18% → 21~25년 18~21%" 밴드의 원출처 미확인.
