# study

학습 워크스페이스 모음. 각 디렉터리가 하나의 주제이고,
[Matt Pocock의 `teach` 스킬](https://github.com/mattpocock) 규약을 따른다.

목표는 노트를 쌓는 것이 아니라 **압축된 학습 결과물**을 남기는 것이다 —
레슨은 한 번 하고 지나가지만, 참조 문서는 계속 다시 열게 된다.

## 웹에서 보기

<https://eatingbug.github.io/study/>

레슨과 참조 문서를 브라우저에서 바로 읽을 수 있다. `main` 에 푸시하면
[GitHub Actions 워크플로](./.github/workflows/pages.yml)가 저장소를 그대로 정적 사이트로 배포한다
(Jekyll 빌드 없음 — 루트의 `.nojekyll` 참조).

> **처음 한 번만:** 저장소 Settings → Pages → **Source** 를 `GitHub Actions` 로 바꿔야
> 워크플로가 배포 권한을 얻는다. 그 뒤로는 푸시할 때마다 자동으로 갱신된다.

사이트 구조는 디렉터리 구조 그대로다 — 루트에 전체 목록,
`/llmops/` 와 `/valley/` 에 워크스페이스별 목록.
`MISSION.md` 같은 마크다운 문서는 GitHub에서 렌더링해 읽는 게 낫기 때문에
목록에서 GitHub 쪽으로 링크한다.

## 워크스페이스

| 주제 | 내용 | 상태 |
|---|---|---|
| [`llmops/`](./llmops) | LLM 운영 체계 — 평가·관측성·비용·배포 | 진행 중 (레슨 2) |
| [`valley/`](./valley) | 기업가치 평가 — DCF·할인율 | 진행 중 (레슨 1) |

## 각 워크스페이스의 구조

```
<topic>/
├── index.html          이 워크스페이스의 목록 페이지 (Pages 진입점)
├── MISSION.md          왜 이걸 배우는가. 모든 레슨이 여기로 소급된다
├── NOTES.md            학습 선호·제약·결정 기록
├── RESOURCES.md        고신뢰 1차 자료 + 커뮤니티 + 아직 못 채운 Gap
├── GLOSSARY.md         이 주제의 표준 용어 (이해가 증명된 것만 등재)
├── lessons/            0001-*.html — 한 번에 하나씩, 짧게, 인터랙티브
├── reference/          압축된 참조 문서. 프린트해서 옆에 두는 용도
├── learning-records/   무엇을 알게 됐고 그래서 다음에 뭘 배울지 (ADR 형식)
└── assets/             레슨이 공유하는 스타일시트·퀴즈 위젯 등
```

레슨과 참조 문서는 HTML이다. 위의 [배포된 사이트](https://eatingbug.github.io/study/)에서 읽거나
로컬 파일을 브라우저에서 바로 열면 된다. 인쇄용 스타일도 들어 있다.

```sh
open llmops/lessons/0001-llmops-map-and-self-audit.html
```

각 워크스페이스의 `index.html` 은 그 워크스페이스의 목록 페이지고,
루트의 `index.html` 은 전체 목록이다.

## 저장소에 넣지 않는 것

- `raw/` — 저작권 있는 원본 자료(유료 구독 콘텐츠 등). 로컬에만 둔다.
- 실습에 쓴 사내 데이터·로그·CSV. 결과 **숫자**만 학습기록에 옮겨 적는다.

자세한 규칙은 [`.gitignore`](./.gitignore) 참조.
