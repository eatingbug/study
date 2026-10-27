# AGENTS.md

학습은 [teach 스킬](./.claude/skills/teach/SKILL.md)을 따른다.
이 저장소는 여러 주제를 포함한다. 선택한 주제의 디렉터리를 학습 워크스페이스로 사용한다.

- 레슨·참조 문서·MISSION을 작성할 때는 [문체 규칙](./docs/writing-style.md)을 읽는다.
- 사내 데이터·로그·원자료는 커밋하지 않는다. 허용된 집계 숫자나 명시한 합성 예시만 남긴다.
- 모든 변경은 브랜치와 PR로 낸다. 접두사는 `lesson/`(레슨·참조), `system/`(학습 시스템),
  `fix/`(오타·링크·스타일)를 쓴다. main에 직접 커밋하지 않는다.
- `index.html`과 `<topic>/index.html`은 생성물이다. 목록 변경은 `python3 tools/build-index.py`로 생성하고
  `python3 tools/build-index.py --check`로 확인한다. 학습자용 문서를 바꿨으면 문체 검사도 실행한다.
