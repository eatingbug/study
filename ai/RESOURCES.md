# AI Engineer + 학습 시스템 Resources

두 갈래다. **학습법**은 인지심리학 1차 문헌에서, **직무 기준**은 실제 채용 루프를 기술한 자료에서 가져온다.
파라메트릭 기억은 쓰지 않는다 — 특히 "AI가 학습에 미치는 영향"은 최근 3년 안에 실증이 쏟아진 영역이라 직감이 가장 잘 틀린다.

## Knowledge — 학습 과학 (1차)

- [Soderstrom, N. C., & Bjork, R. A. (2015). *Learning versus Performance: An Integrative Review.* Perspectives on Psychological Science, 10(2), 176–199.](https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/11/soderstorm_ra_learningvsperformance.pdf)
  이 워크스페이스 전체의 뼈대. **performance(지금 관찰되는 수행) ≠ learning(지속되는 변화)** 이며, 수행은 학습의 신뢰할 수 없는 지표라는 리뷰. 쓸 곳: 어떤 학습 활동이 "잘 되는 느낌"인데 남지 않는지 판단할 때.
- [Bjork, E. L., & Bjork, R. A. (2023). *Introducing Desirable Difficulties Into Practice and Instruction: Obstacles and Opportunities.* In Overson, Hakala, Kordonowy & Benassi (Eds.), *In Their Own Words*, APA Division 2, pp.19–21.](https://www.unh.edu/teaching-learning-resource-hub/sites/default/files/media/2023-06/itow-introducing-desirable-difficulties-into-practice-and-instruction-bjork-and-bjork.pdf)
  **New Theory of Disuse**: 저장 강도 / 인출 강도 2요인과 그 **비대칭** — *"인출 강도가 높을수록 재학습·인출에서 얻는 저장 강도 증가분은 작아진다"*(p.20). "망각은 학습의 친구", "인출 > 재학습", 교차로 시간 손실 없이 간격 만들기, 그리고 25년간 이 조언이 **안 먹힌 이유**(desirable difficulties are typically undesired). 쓸 곳: 모든 레슨의 설계 원리. ⚠️ WebFetch로는 추출이 깨진다 — `pdftotext -layout`으로 긁을 것.
- [Cepeda, N. J., Vul, E., Rohrer, D., Wixted, J. T., & Pashler, H. (2008). *Spacing Effects in Learning: A Temporal Ridgeline of Optimal Retention.* Psychological Science, 19(11), 1095–1102.](https://files.eric.ed.gov/fulltext/ED505660.pdf)
  1,350명 이상, 간격 최대 3.5개월 / 시험 지연 최대 1년. **최적 간격의 실제 숫자**: RI 7·35·70·350일 → 1·11·21·21일. RI 70일에서 간격 0일 대비 회상 **+111%**. 초록: 최적 간격은 몇 주 지연에 약 20%, 1년 지연에 약 5%. 쓸 곳: 복습 일정의 근거 (`assets/schedule.js`가 이 능선을 보간한다). ⚠️ 재료는 **사실 쌍**이지 시스템 판단이 아니다 — 전이는 가정이다.
- [Kornell, N., Hays, M. J., & Bjork, R. A. (2009). *Unsuccessful Retrieval Attempts Enhance Subsequent Learning.* JEP: Learning, Memory, and Cognition, 35(4), 989–998.](https://web.williams.edu/Psychology/Faculty/Kornell/Publications/Kornell.Hays.Bjork.2009.pdf)
  **답할 수 없게 설계된** 문제에서도 인출을 시도한 쪽이 이후 학습이 좋았다(실험 6개). 쓸 곳: "30초 규칙" — AI에게 묻기 전에 틀린 답이라도 먼저 쓰라는 처방의 근거.
- [Fan, Y., Tang, L., Le, H., Shen, K., Tan, S., Zhao, Y., Shen, Y., Li, X., & Gašević, D. (2025). *Beware of Metacognitive Laziness: Effects of Generative AI on Learning Motivation, Processes, and Performance.* British Journal of Educational Technology, 56(2).](https://bera-journals.onlinelibrary.wiley.com/doi/10.1111/bjet.13544) ([arXiv 프리프린트](https://arxiv.org/abs/2412.09315))
  대학생 117명 RCT. ChatGPT 집단 / 인간 전문가 / 작문 분석 툴 / 무지원 4조건. **ChatGPT 집단은 에세이 점수 향상에서 앞섰으나 knowledge gain·transfer는 유의차 없음.** 워크스페이스의 핵심 인용. 쓸 곳: "AI를 쓰면 왜 실력이 안 느는가"의 유일한 실증 근거.
- [Barcaui, A. — *ChatGPT as a Cognitive Crutch: Evidence from a Randomized Controlled Trial on Knowledge Retention* (SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5353041)
  파지(retention)에 초점을 맞춘 별도 RCT. 위 결과의 **독립 재현**으로 쓸 것 — 단일 연구에 기대지 않기 위해.

## Knowledge — 직무 기준 (무엇이 실제로 평가되는가)

- [KORE1 — *LLM Engineer Interview Questions: 2026 Hiring Guide*](https://www.kore1.com/llm-engineer-interview-questions/)
  **6개 역량**(검색/RAG · 평가 · 비용·레이턴시 · 안전성/프롬프트 인젝션 · 파인튜닝 판단 · 시스템 판단)과 각각의 합격 신호/불합격 신호를 질문 단위로 기술. 동시에 **과잉 테스트되는 저가치 영역**(트랜스포머 내부, 토크나이저, PyTorch 밑바닥)을 명시. MISSION의 Success/Out of scope가 여기서 나왔다. 쓸 곳: 커리큘럼 우선순위, 모의 면접 문항.
- [KORE1 — *How to Hire an LLM Engineer in 2026*](https://www.kore1.com/how-to-hire-llm-engineer-2026/)
  고용주 관점의 역할 정의·보상·실무 테스트 설계. 쓸 곳: 이력서/JD 해독, 내 포지셔닝 문장 쓰기.
- [Aced(구 Exponent) — *45+ AI Engineer Interview Questions & Answers (2026)*](https://www.tryexponent.com/blog/ai-engineer-interview-questions)
  OpenAI·Anthropic·Scale·Sierra·Databricks 등 실제 루프에서 나온 문항 모음(추론 배칭 설계, 에이전트 설계 등). 쓸 곳: 시스템 디자인 드릴 원재료. ⚠️ 커리어 서비스 매체 재게시본이 여러 개 돌아다닌다 — 원문 기준으로 볼 것.

## Wisdom (Communities)

아직 사용자와 합의되지 않음. 다음 세션에서 의사 확인 후 확정한다. 후보:

- **Latent Space (Discord + 뉴스레터/팟캐스트)** — "AI Engineer"라는 직무명을 정착시킨 곳. 제품 엔지니어 층의 밀도가 가장 높다.
- **r/LocalLLaMA** — 서빙·추론 최적화·양자화 실무 신호. 인프라 축에 유용.
- **국내: 모두의연구소 / GDG·AWS UG의 LLM 밋업, 판교 LLM 스터디** — 한국어 레퍼런스 체크와 이직 시장 정보.
- **기술 블로그 자체가 커뮤니티 진입로** — velog/Medium 발행 후 피드백을 받는 경로.

## Gaps

- **AI 인프라/플랫폼 축의 1차 자료가 없다.** 추론 서버(vLLM/TGI), 배칭, KV 캐시, 비용 모델링의 신뢰 가능한 출처를 아직 못 찾았다. 인프라 레슨 전에 반드시 채울 것.
- **Bjork PDF 본문 미확보.** 자동 추출 실패. storage/retrieval strength 정의를 verbatim으로 인용하려면 직접 읽어야 한다.
- **한국 시장의 AI Engineer JD 실물**이 없다. 사용자가 실제 관심 있는 회사 JD 3~5개를 모아 오면 커리큘럼을 그쪽으로 조준할 수 있다.
