# LLMOps Resources

미션(→ [MISSION.md](./MISSION.md))에 맞춘 고신뢰 자료만 남긴다. 링크만 있는 항목은 3개월 뒤 쓸모없다 — 반드시 한 줄 주석을 붙인다.

## Knowledge

### 평가 (Eval) — 최우선 영역

- [LLM Evals: Everything You Need to Know — Hamel Husain & Shreya Shankar](https://hamel.dev/blog/posts/evals-faq/)
  이 분야의 사실상 표준 문서. 7개 섹션 FAQ 형태. **Use for**: 오류분석(error analysis) 절차,
  binary vs Likert 판정 설계, 트레이스 몇 개를 봐야 하는가, judge 정렬(TPR/TNR) 측정.
  핵심 인용: *"Error analysis is the most important activity in evals. Error analysis helps you decide
  what evals to write in the first place."* / *"you should aim to review at least 100 traces…
  if ~20 traces don't turn up a new category, you can stop"*
- [PDF 버전 (오프라인/프린트용)](https://hamel.dev/blog/posts/evals-faq/evals-faq.pdf)
  통근길 읽기용. 내용 동일.
- [Q: What are LLM Evals? — Hamel Husain](https://hamel.dev/blog/posts/evals-faq/what-are-llm-evals.html)
  "eval"이라는 단어가 사람마다 다른 뜻으로 쓰이는 문제를 정리. **Use for**: 글 쓸 때 용어 정의 문단.
- [Evals, error analysis, and better prompts — Lenny's Newsletter (Hamel 인터뷰)](https://www.lennysnewsletter.com/p/evals-error-analysis-and-better-prompts)
  실제 클라이언트(Nurture Boss) 사례가 나온다. **Use for**: "vibe check에서 벗어나는" 서사 예시.

### 전체 지도 / AI 엔지니어링

- [Building LLM applications for production — Chip Huyen](https://huyenchip.com/2023/04/11/llm-engineering.html)
  프로덕션화의 난점을 처음 체계적으로 정리한 글. 2023년이라 도구 이야기는 낡았지만
  **문제의 구조**(프롬프트 모호성·버전관리·비용/지연·태스크 조합)는 지금도 유효.
  **Use for**: "왜 LLM은 운영이 어려운가" 논거.
- [The AI Engineering Stack — Gergely Orosz × Chip Huyen](https://newsletter.pragmaticengineer.com/p/the-ai-engineering-stack)
  스택을 application / application development / model development / infrastructure 4층으로 자른다.
  **Use for**: 내 역할이 어느 층에 있는지 위치 잡기.
- Book: _AI Engineering_ — Chip Huyen (O'Reilly, 2025)
  위 블로그 글들의 확장판. **Use for**: 영역별로 깊이 들어갈 때의 레퍼런스 서적.
- [Building an LLM evaluation harness — Hamel × Shreya 마스터클래스 정리](https://www.aakashg.com/ai-evals-masterclass-with-hamel-shreya/)
  강의 내용을 단계별로 요약. **Use for**: 커리큘럼 순서 검증용 대조 자료.

### 영어 작문 자동채점 (AES) — 사용자의 프로덕션 도메인

> 사용자의 LLM 기능은 **루브릭 기반 영어 작문 채점**이다. 즉 프로덕션 시스템 자체가 judge다.
> 이 섹션이 이 워크스페이스의 중심 자료다.

- [Investigating first-language bias in LLM-based automated essay scoring: A cross-prompt
  evaluation of an open-weight model on TOEFL essays](https://arxiv.org/html/2607.14605) — arXiv
  **이 워크스페이스에서 가장 중요한 논문.** Gemma-3-27B + LoRA, TOEFL11 코퍼스(12,100편, L1 11종, 미출제 프롬프트 8개).
  **Use for**: 한국인 학습자 채점의 L1 편향 가설을 세우고 우리 데이터로 재현하기.
  검증된 수치:
  - 전체: 정확 밴드 일치 77.79%, QWK 0.702, 인접 밴드 정확도 99.98%
  - **L1 연동 점수 오프셋이 세 밴드 전부에서 유지됨.** 유럽어권(독·불·이·스) > 동아시아권(일·한·중)
  - 격차: +0.21점(하) / +0.33(중) / +0.30(상). 표준화 오프셋 **독일어 +0.55 ↔ 한국어·일본어 −0.34**
  - 밴드 간 L1 평균점수 순위상관이 강함 (ρ=0.88~0.96) → 우연이 아니라 체계적 편향
  - 파인튜닝 데이터 구성 탓이 아님 (학습 노출량과 오프셋 상관 r=−0.34, p=.183, 부호도 반대)
  - ⚠️ 주의해서 읽을 지점: 하위 밴드에서 ETS 일치율은 동아시아 66.0% > 유럽 48.3%.
    즉 "동아시아권을 못 맞힌다"가 아니라 **밴드 내 원점수를 낮게 준다**는 것. 인용 시 혼동하지 말 것.

- [Evaluating Quadratic Weighted Kappa as the Standard Performance Metric for AES](https://educationaldatamining.org/EDM2023/proceedings/2023.EDM-long-papers.9/index.html) — EDM 2023
  QWK를 유일 지표로 쓰면 안 되는 이유. **Use for**: 우리 채점기 성능을 보고할 때 지표 선택 근거.
  - **kappa paradox**: 퍼센트 일치 99.8%인데 QWK 0.488이 나올 수 있다
  - 척도 민감성: 사람 점수를 합/평균/최댓값으로 합치는 방식만 바꿔도 QWK가 흔들린다 (합 > 평균·최댓값)
  - 대각선 내 일치 **위치**에 따라 정확도가 같은데도 QWK 0.599 ↔ 0.855로 요동
  - 대안: Linear Weighted Kappa, 3인 이상이면 Fleiss' kappa / Krippendorff's alpha
  - 결론: **여러 지표를 함께 쓸 것.** QWK 단독 금지.

- [Auditing Multimodal LLM Raters: Central Tendency Bias in Clinical Ordinal Scoring](https://arxiv.org/pdf/2605.16386) — arXiv
  LLM이 서열 척도를 매길 때 **양 극단을 회피하고 중간 밴드로 몰리는** 현상.
  **Use for**: 우리 채점 분포가 중간에 뭉쳐 있는지 검사 (히스토그램 한 장으로 탐지 가능).
  탐지법: 점수 분포를 기대 분포와 비교 + 전체 혼동행렬(confusion matrix) 확인.
  완화: 척도 전 범위를 쓰라고 명시하는 프롬프트, 모델 교체.

- [Agreement Between LLMs and Human Raters in Essay Scoring: A Research Synthesis](https://www.researchgate.net/publication/398766141_Agreement_Between_Large_Language_Models_and_Human_Raters_in_Essay_Scoring_A_Research_Synthesis)
  여러 연구의 메타 정리. **Use for**: 우리 수치가 업계 대비 어디쯤인지 감 잡기.
  요지: LLM–사람 일치도는 대체로 **QWK/상관 0.30~0.80** 구간. 연구 간 편차가 크고 보고 관행이 표준화돼 있지 않다.
- [Fairness in Automated Essay Scoring](https://aclanthology.org/2024.bea-1.18.pdf) — ACL BEA 워크숍
  AES 공정성 측정 프레임. **Use for**: 편향을 "지표"로 정의하는 방법.
- [Automated Refinement of Essay Scoring Rubrics via Reflect-and-Revise](https://arxiv.org/html/2510.09030)
  사람 점수 200편을 써서 루브릭 자체를 반복 개선. TOEFL11/ASAP에서 QWK 최대 +0.19 / +0.47.
  **Use for**: 프롬프트를 손대는 대신 **루브릭 문서를 개선**하는 접근. 나중 레슨용.

### LLM-as-judge 편향 (일반)

- [Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge](https://arxiv.org/pdf/2410.02736)
  judge 편향 분류의 표준 참조. **Use for**: 편향 종류 어휘 정리.
- [Evaluating Scoring Bias in LLM-as-a-Judge](https://arxiv.org/pdf/2506.22316)
  대부분의 judge 연구가 쌍대비교(pairwise)인데, 이 논문은 **점수 매기기(scoring)** 편향을 다룬다 — 우리 케이스.
  ⚠️ **주의**: verbosity/position 편향과 그 완화책(swap augmentation, balanced position calibration)은
  **쌍대비교 judge용**이다. 단일 응답 루브릭 채점에는 그대로 적용되지 않는다 — 잘못 가져오지 말 것.

### 관측성 (Observability)

- [OpenTelemetry GenAI Semantic Conventions — MLflow 문서](https://mlflow.org/docs/latest/genai/tracing/opentelemetry/genai-semconv/)
  `gen_ai.*` 속성 규약의 실제 필드를 확인할 수 있는 문서. **Use for**: 트레이스 스팬 설계,
  벤더 종속 없이 로그 스키마 잡기. (v1.37+ stable, v1.41.0에서 reasoning token 속성 추가)
- [How OpenTelemetry Traces LLM Calls, Agent Reasoning, and MCP Tools — Greptime](https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions)
  LLM client span / agent span / event / metric 4분류를 코드와 함께 설명. **Use for**: 실습 시 스팬 구조 참고.
- [Top Open Source LLM Observability Tools 2026](https://openobserve.ai/blog/llm-observability-tools/)
  ⚠️ 벤더 블로그 — 편향 감안. **Use for**: 도구 이름과 라이선스 확인용(팩트만).
  현 시점 요지: Langfuse(MIT, self-host 표준) / Arize Phoenix(OTel-native, Elastic v2) /
  Braintrust(SaaS, CI 게이트 강점) / Opik·MLflow(Apache 2.0).

## Wisdom (Communities)

- [Latent.Space Discord & LLM Paper Club](https://www.latent.space/p/community)
  swyx 운영. 2026년 기준 applied AI engineering 논의의 중심. 매주 논문 클럽.
  **Use for**: 내 평가 설계·아키텍처 결정을 실무자에게 비평받기, 글 발행 전 사전 검증.
- [Instruct.KR](https://luma.com/sj78l1dz)
  국내 AI 연구자·엔지니어·프로덕트 팀 커뮤니티. LLM 훈련/배포 현장 경험 공유, 오프라인 밋업.
  **Use for**: 한국어 서비스 특수성(토크나이저·존댓말·도메인 용어) 논의, 국내 인지도 쌓기.
- [파이토치 한국 사용자 모임](https://pytorch.kr/)
  국내 최대 규모. 서빙·추론 최적화 쪽 글이 올라온다. **Use for**: 서빙 영역 학습 시 질문 창구.

## Gaps

아직 좋은 자료를 찾지 못한 영역 — 다음 세션의 검색 대상:

- **프롬프트 버전관리 · CI 게이트**: 벤더 문서 외에 원칙을 다룬 1차 자료가 없다.
  eval을 PR 게이트로 쓰는 실제 사례 글이 필요.
- ~~**RAG 운영 평가**~~ — **탐색 보류** (2026-08-04, 프로젝트 우선순위 하향).
  되살릴 때 찾을 것: retrieval 품질과 generation 품질을 분리 측정하는 방법론 1차 자료
  (RAGAS 논문 / IR 평가 지표 원전).
- **비용·토큰 예산 관리**: 캐싱·라우팅·배치의 트레이드오프를 숫자로 다룬 실무 글.
- **채점기를 프로덕션에서 모니터링한 실무 사례**: 위 논문들은 전부 오프라인 벤치마크다.
  "배포된 채점기의 점수 드리프트를 어떻게 감시하는가"에 대한 1차 자료가 없다.
  ← 우리가 실제로 하고 나면 그게 자료가 된다.
- **한국인 학습자 대상 LLM 영어 작문 채점** — 한국어로 쓰인 실무 자료가 사실상 없다.
  L1 편향(위 arXiv 2607.14605) 재현 + 우리 데이터 결과는 **블로그의 최대 차별점이다.**
  국내 영어교육 도메인 + LLM 운영 경험을 동시에 가진 사람이 드물다.
